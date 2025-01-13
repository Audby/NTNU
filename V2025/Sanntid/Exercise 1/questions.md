Exercise 1 - Theory questions
-----------------------------

### Concepts

What is the difference between *concurrency* and *parallelism*?
> "Concurrency" er der man setter opp oppgaver som skal utføres og løses uavhengig av hverandre. Parallellisme er der flere ulike oppgaver utføres samtidig, som på ulike kjerner i en prosessor.

What is the difference between a *race condition* and a *data race*? 
> En race condition er der utfallet av én hendelse er avhengig av utførelsen av en annen hendelse, som derfor danner uønsket oppførsel, mens "data race" er der to eller flere tråder prøveer å få tilgang på en variabel uten ordentlig synkronisering.
 
*Very* roughly - what does a *scheduler* do, and how does it do it?
>  En scheduler er der for å bestemme nøyaktig rekkefølge og timing på oppgavene som utføres.


### Engineering

Why would we use multiple threads? What kinds of problems do threads solve?
> Bruker flere ulike tråder samtidig for å kunne utføre flere oppgaver samtidig, og dermed forbedre respons og tidsbruk når man kjører et program.

Some languages support "fibers" (sometimes called "green threads") or "coroutines"? What are they, and why would we rather use them over threads?
> Fibere er tråder som er lettere å operere og kan derfor times ved hjelp av scheduler i stedet for det underliggende operativsystemet. 

Does creating concurrent programs make the programmer's life easier? Harder? Maybe both?
> Det gjør det mye enklere å gjøre et program effektivt, som er en god ting, men legger også til kompleksitet som kan forårsake bugs og error.

What do you think is best - *shared variables* or *message passing*?
> Jeg vil tro begge kan være det beste valget avhengig av bruksområdet. Delte variabler krever nøye synkronisering for å virke ordentlig, men er ganske enkelt å implementere. Message passing kan være mer robust for større applikasjoner, men er også mer komplisert å implementere.


