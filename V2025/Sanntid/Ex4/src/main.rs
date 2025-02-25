use std::net::UdpSocket;
use std::time::{Duration, Instant};
use std::{env, process, thread};
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;
use std::process::{Command, Stdio};

// Configuration for heartbeat and timeout durations.
const HEARTBEAT_INTERVAL: Duration = Duration::from_millis(500);
const HEARTBEAT_TIMEOUT: Duration = Duration::from_secs(2);

// UDP address used for heartbeat communication.
const HEARTBEAT_ADDR: &str = "127.0.0.1:34254";

// Helper function to spawn a backup process.
fn spawn_backup() {
    let exe = env::current_exe().expect("Failed to get current executable");
    // Spawn a new instance with the "--backup" flag.
    /* Linux version:
        let childy = Command::new("xterm")
            .arg("-e")          // Execute a command in the new terminal
            .arg("Monospace")  // Use Monospace font or another standard font
            .arg(format!("{} --backup", exe.display())) // Launch backup in new terminal
            //.stdout(Stdio::inherit()) // Show stdout in the main process
            //.stderr(Stdio::inherit()) // Show stderr in the main process
            .spawn()
            .expect("Failed to spawn backup process");

        println!("child id {}", childy.id());
     */

    // Windows version:
    let child = Command::new("cmd")
        .args(&["/C", "start", exe.to_str().unwrap(), "--backup"])
        .spawn()
        .expect("Failed to spawn backup process");
    
    println!("child id {}", child.id());
}

fn main() {
    // Determine the role based on command-line arguments.
    let args: Vec<String> = env::args().collect();
    let is_backup = args.iter().any(|arg| arg == "--backup");

    // The counter state, shared (atomically) within a process.
    let counter = Arc::new(AtomicU64::new(1));

    if !is_backup {
        // In the primary, we spawn the backup process immediately.
        spawn_backup();

    }

    if is_backup {
        // Backup process: Bind to the heartbeat address to listen for messages.
        let socket = UdpSocket::bind(HEARTBEAT_ADDR)
            .expect("Backup: Could not bind to heartbeat address");
        // Set a read timeout so we can detect missing heartbeats.
        socket
            .set_read_timeout(Some(HEARTBEAT_INTERVAL))
            .expect("Failed to set read timeout");

        let mut last_heartbeat = Instant::now();

        loop {
            let mut buf = [0; 32];
            match socket.recv(&mut buf) {
                Ok(n) => {
                    // Parse the counter value sent in the heartbeat.
                    if let Ok(msg) = std::str::from_utf8(&buf[..n]) {
                        if let Ok(value) = msg.trim().parse::<u64>() {
                            // Update the counter so we can continue where primary left off.
                            counter.store(value, Ordering::SeqCst);
                        }
                    }
                    // Refresh our heartbeat timer.
                    last_heartbeat = Instant::now();
                    println!("Recieved heartbeat, refreshing heartbeat timer")
                }
                Err(ref e) if e.kind() == std::io::ErrorKind::WouldBlock => {
                    // Read timeout reached – do nothing and check below.
                }
                Err(e) => {
                    eprintln!("Backup: Error receiving heartbeat: {}", e);
                }
            }

            // If too much time has passed since the last heartbeat, assume primary failure.
            if last_heartbeat.elapsed() > HEARTBEAT_TIMEOUT {
                println!("Backup: No heartbeat detected. Promoting self to primary.");
                // Spawn a new backup for the future.
                spawn_backup();
                // Break out of the backup loop to become primary.
                break;
            }
        }
    }

    // Now we are (or have become) the primary.
    // For heartbeat sending, we bind a socket to an ephemeral port and connect to HEARTBEAT_ADDR.
    let heartbeat_socket = UdpSocket::bind("127.0.0.1:0").expect("Primary: Could not bind UDP socket");
    heartbeat_socket
        .connect(HEARTBEAT_ADDR)
        .expect("Primary: Could not connect to heartbeat address");

    // Main loop: print the counter, send heartbeat, and then sleep.
    loop {
        // Get and increment the counter atomically.
        let current = counter.fetch_add(1, Ordering::SeqCst);
        println!("{}", current);

        // Send the current counter value as a heartbeat message.
        let msg = current.to_string();
        if let Err(e) = heartbeat_socket.send(msg.as_bytes()) {
            eprintln!("Primary: Failed to send heartbeat: {}", e);
        }

        // Sleep before printing the next number.
        thread::sleep(Duration::from_secs(1));
    }
}
