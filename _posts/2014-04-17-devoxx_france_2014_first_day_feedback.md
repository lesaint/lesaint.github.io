---
layout: post
title: Devoxx France 2014, first day feedback
tags: Devoxx Java8 Docker Redis JBossForge BlueTooth
categories: articles
image:
 feature: feature_image_green.png
---

On Wednesday 16 of April, I went to the first day of Devoxx France 2014 in Paris. This university day was indeed crowded and choosing between session
was tough.


## Hands-on-lab: Docker by Julien Vey et Pierre Padrixe

Nice session. True hands-on session with a nice tutorial progressively diving into Docker towards a real world use case : a Docker container with a Git
repository which will trigger a build on a Docker container containing a Jenkins server via a git-hook.

I don't think many attendees went to the end of the tutorial, especially those like me who had never worked with docker before, but the whole tutorial
is on [Github](git@github.com:julienvey/docker-hands-on.git) with the target solution and can be finished later.

Thanks the Julien Vey for their support. Good thinking setting up a VM to share on USB key during the session to get everyone started quickly.

## University: Java 8, Streams & Collector by José Paumard (@JosePaumard)

José's university was very well prepared and very interesting, going nicely and progressively into the new feature of Java8, featured with detailed
and intuitive explanations and illustrated by funny and far from pointless practical exercises with live coding on stage.

The presentation will obviously on Parleys but José (and Remy Forax) were kind enough to answer several questions off-stage that I will report here.

### Streams can not be reused

José quickly said something about `Stream` not being reusable during a live coding session.

Coming from the world of Guava where `Iterable<T>` can be stored in variable and reused, this statement felt very surprising to me.

But indeed, Remy Forax pointed out that Streams implementation is very different from the Iterables, notably because they are implemented at the
JVM level and are capable of optimisations (among which parallelism and use of lambda) much more powerful than Guava has ever been capable of.
The way they are implemented just isn't compatible with reuse. More specifically, when a stream has been consumed, any attempt to reuse it will
throw an `IllegalStateException`.

### replacing the Collect([...]).entrySet().stream()

### Question 1

Dans le cas d'une source de donnée par nature séqentielle est-il possible de collecte (ie. aggréger des données) sans rompre le stream ?
Si cette une source de donnée de taille indéfini et potentiellement très importante, cela évite de créer une Map en mémoire inutilement.

#### Question 1.a

Un stream sur un fichier est-il bien séquentielle ? dans tous les cas ? Un accès parallèle à plusieurs partie d'un même fichier,
si on ne s'intéresse pas à l'ordre des données peut être une grosse optimisation.

## Tools in Action: Redis, une base Not Only NOSQL by Nicolas Martignole (@nmartignole)

Nicolas did an excellent work at describing and pointing out the strong advantages and the simplicity of Redis.

Illustrated by several use cases, the main of which was the own Devoxx CFP's website, this presentation gave me a pretty good idea of how to
use Redis and I really bought the easy of access and performance awareness of the product

I will definitely try it.

## Tools in Action: JBoss Forge in Action by Antonio Goncalvez

My overall feeling about this presentation was that it was a little messy. Antonio had several technical problems.

Still, it was successful at giving a good idea of what JBoss Forge is (and isn't) and a high ground idea of how it is architectured.

## Tools in Action: Bluetooth Low Energy by Romain Menetrier (@romemore)

I went to this session out of curiosity.
I don't intend to work on bluetooth any time soon but I expected this session to give me an idea of what bluetooth is nowadays and how it can be
implemented.

And I was satisfied on those points with the presentation of Romain Menetrier. It was worth the time.


