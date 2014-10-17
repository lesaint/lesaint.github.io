---
layout: post
title: Devoxx France 2014, second and last day feedback
tags:
 - Devoxx
 - Java8
 - Gradle
 - Cassandra
 - WebSocket
 - Bitcoin
categories: articles
image:
 feature: feature_image_green.png
redirect_from:
  - /2014/04/18/devoxx_france_2014_second_and_last_day_feedback.html
comments: true
---

This was my second and last day at Devoxx France 2014.

But it was the "real" first day of Devoxx which started by a word of the Devoxx team, funny but also instructive as they dropped the news of Devoxx 2015
leaving the Mariott for a much bigger place : le Palais des congrés de la Porte Maillot.

I also enjoyed the keynotes, especially the surprise word of Tariq Krim which gives hope of France recognising the asset which are the french developers.


== Gradle ne fait pas que remplacer Maven by Cedric Champeau (@CedricChampeau)

Cedric's presentation on Gradle was quite polluted with too much trolling and comparison with Maven.
Fortunately, it went better after half the presentation when he started actually showing what Gradle is capable of and how it does it.

Cedric admitted he had to skip some parts of his presentation of some features. In my opinion, the reason comes from too much time lost on giving reason of his bad opinion of Maven.

Still, overall, I think I got a good idea of the product and want to try it out.

== Les concepts de la programmation fonctionnelle illustrés avec Java 8 by Yannick Chartois (@ychartois)

I did not learn much from this quickly since I already know functional programming paradigms and now have a pretty good knowledge of Java 8 from José Paumard presentation the day before and other source of information about lambda before Devoxx.

Still, the presentation was well prepared and it wasn't a strong waste of time to do a global overview of functional programming in Java 8.

== Les applications réactives : un nouveau paradigme pour relever les défis de l'économie numérique by Fabrice Croiseaux et Antoine Detante

Interesting presentation about both the concepts behind the buzzword "Reactive Programming" and the patterns to implement them.

The presentation included code samples in several languages, from Scala to Javascript, which very practically pointed that reactive is about patterns which can be implemented today.

This was a very good introduction to the Reactive concepts and their business advantages.

Lire le Reactive Manifesto

== Cassandra, une nouvelle ère by Jonathan Ellis

I didn't know cassandra. I don't know how to use it any more than before this presentation, but now I'm really convinced of the powers and strength of this product.

Jonathan did an excellent presentation, clear and with a pretty good french (even though he is american).
He quoted three major companies about the reasons they choose cassandra, each for different and complementary reasons.

Jonathan completed this with graphics and explanations about the technical paradigms and algorithm used to achieved near perfect availability, extremely low latency and other killing features.

I will keep Cassandra in mind.
After the presentation about Redis the day before, I am now aware of two database products I didn't know before and when to use each one.
I am very happy with that.

== Vive les WebSockets libres! by Jean-François Arcand (@jfarcand)

Jean-François comes from Quebec. As one would expect from a quebecois to make a presentation entertaining for a french audience from France,
he has a strong accent and jumps on any opportunity to make fun on our use of english words (such as "browser" when in Quebec, they say "fureteurs").

He is also (and mainly) the creator (?) of the Atmosphere framework.

That said, he is in a very good position to make an interesting, well documented and critical presentation on WebSocket (and sell Atmosphere, in the process).

Now I know many of the many pitfalls of implementing websocket when the JSR isn't even finished, when browser and proxies are very inconsistent in how they treat them and when on the Internet barely half of the users use a websocket-enabled browser.

== Building a real time risk analysis system in Java by Alexandre Navarro (@alex_j_navarro) and Benoît Lacelle (@benoit_lacelle)

Docker conference room was full 10 minutes before the conference started. I've been to the university on the subject so no regret. Kick-ass conference seems to be the same I have seen online.
So I went to this conference out of lot of curiosity and to get me out of my comfort zone.

At the beginning, I was very much uncomfortable with the subject because the conference looked a lot like a commercial show for about a closed source product.

But after a while, the speech went deeper into the many challenges of computing indicators from real time multi-dimensional data updating at a very high frequency.

I must say that it was a good opportunity to learn about the scale of some existing solutions in the banking world
(Apparently, a 80Gb heap JVM is considered a small JVM at la Société Générale...), but I didn't learn much for my day-to-day work.

== Bitcoin et monnaies cryptographiques by Gregory Paul (@paulgreg)

This conference is the one I will certainly remember as the one from which I learned the most and as the most complete on its subject.

Gregory's conference was well organised and covered every aspect I could have had a question about on the subject of bitcoins.

It covered the cryptographic principles behind the money, how transactions work and how they are secured, history of bitcoin, how to get mine and what it costs today,
the other crypto moneys and why they were created, the current eco system around bitcoin, how the money could be destroyed, etc...
