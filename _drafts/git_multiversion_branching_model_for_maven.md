---
layout: post
title: Git multiversion branching model for maven
description: A branching and merging model for Git for application with multiple concurrent versions, managed with Maven
tags: git maven
---

The following Branch and Merge model for Git has the following goals :

* having multiple concurrent version of a project as a base concept
* support for Maven and version number beeing in the source (ie. in pom.xml files)
* support for project in which version numbers matters (because its important for the customer or because of dependency management)
* make the merge/branching operation as simple and as few in number as possible
* beeing a convenient ground for using continuus build with as little maintenance as possible

## Abtract

In this article, we will discuss the following points in order :

* The death of the master branch
* Layered by version branching model
* Horizontal merges
* Vertical merges
* Where is my history ?
* Feature branching
* Merging feature branches

## The death of the master branch

The [Git-Flow]() is probably the most famous branching model for Git and one of the key element is the use of the master branch as a reference branch for the project.

(include citation du git flow)

But, when dealing with a project which basic development model is having multiple versions at the same time, maintaning such a branch ends up beeing a vow of faith.
It is possible, but it is just not what you need Git on your every day work.






In the world of Git, one on the most famous and used model for branches, merges and releases is the [Git-Flow]().
But it is essentially thought for projects/applications with one single reference version at a time.
Also, it does not address the problem of having the version explictly managed inside the version controled sources, as the Maven pom.xml files do, and

The following article attemps at providing a simple (as with at least principles as possible) Git branching and merging model
which takles with the problem of dealing with more than one version at a time and Maven.

## Abtract

In this article, we will discuss the following points in order :

* Maven + Git + continuus integration = not easy
* The death of the master branch
* Layered by version branching model
* Horizontal merges
* Vertical merges
* Where is my history ?
* Feature branching
* Merging feature branches

## Maven + Git + continous integration = not easy

For the last year and half, I have been working on two big java-based projects which have in common the following features :

* maven is used for building and managing dependencies
* source is version controlled with Git
* projects have a continus build stack
* most important : more than one version of the product are developped and delivered to the client at the same time

They also add common problems :

* 

By design, Maven deals with version numbers (explicitly written in pom.xml files). Its core behavior is to produce SNAPSHOTs artifacts for "in-progress" pieces of code and non-SNAPSHOT artifacts for final pieces of code.
It also has a complex, yet effective enough, system for dependency mangagement which relies on the SNAPSHOT/RELEASE concept.
Most Java projects use  Maven today (though [Graddle]() seems to take the wind nowadays, but this is another subject).

Also, most teams of at least several Java developers are using a Continuus Build solution to monitor the code for broken builds or tests.

In such circonstances, most (if not all) Java developpement teams have come to face the problem of having branches of java code built 

## The death of the master branch

....
extrait du git flow here defining the master branch
...

I personnaly think it is pointless to have a branch which contains only merges commits and thinks it is a big mistake to have a branch with a non-SNAPSHOT version number.

* on first point : the argument for such a branch is mainly to get some kind of clean historical view in a branch of all the versions
    - what's the point ? You get an even better view by simply listing all the tags and sort them. This is much more synthetical
      (indeed, you need a little consistency in your tag naming, but who hasn't it already ?)
    - in the context of multiple concurrent versions, having such a branch is just inpossible since you can get release of version 8 before the last release of version 7
      also, as we will see later, the latest dev branch will always have all the tagged commits (it won't be convenient to read, I agree), so the history of the whole project is not lost
* on second point : a branch should never stay with a non SNAPSHOT version in the pom.xml
    - if such a branch exists, you are exposed to have it built more than one time
        + case 1 : you either will have the same artifacts produced (ie. pointless build)
        + case 2 : a commit has been pushed to the branch, you then get new artifacts with a different content but with the same version number (ie. big error !)
            * on the damage-side, I agree, there isn't much. Either the repository is correcly written and will reject the new artifacts or you just corrupt your local repository
    - if you need to make a fix on a specific version, use the tag, it is easy to create a branch from it

## Layered by version branching model

## Horizontal merges

## Vertical merges

