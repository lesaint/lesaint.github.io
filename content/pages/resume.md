title: Resume
subtitle: Sébastien Lesaint - Senior Software Engineer & Application Architect
slug: sebastien_lesaint_resume
header_position: 0

[TOC]

# Professional Profile

* Goal-driven technical professional with an illustrated track record of innovation in high quality software development, complex systems modelling, cloud-based architecture, and backend programming for high-traffic servers and services.
* Backend developer with 15 years of expertise in Java development and relational database design and usage, over 3 years of Python programming experience, and diversified skills in infrastructure, CI/CD, software engineering and security.
* Proven leader recognized for strong technical acumen, as well as dynamic problem-solving, communication, interpersonal, analytical, and decision-making skills.
* Eager to learn and adopt new approaches and languages to fulfil requirements particular to unique contexts.
* Demonstrated expertise in technology management, including application server management and knowledge sharing.
* Conversant to industry trends and driving continuous improvement through the adoption of new tools and methodologies.

# Competencies
<dl><dd>Technical Design ▪ Domain Driven Design ▪ Business Rules Analysis ▪ Stakeholder Engagement ▪ Research & Development ▪ Open Source Mindset ▪ Quality Assurance ▪ Production Troubleshooting ▪ Performance Optimization (SQL, CPU/Mem, Cross-Service)</dd></dl>

# Career

## Machine Learning Engineer

[SonarSource](https://www.sonarsource.com/company/about/) ▪ Annecy, France ▪ 2023 - 2024

* Collaborated closely with SonarSource's Machine Learning (ML) scientists, providing integral support to 4 research initiatives, notably through the crafting of cloud-based solutions tailored to their requirements.

**Achievements**

* Advised scientists in 2 ML research studies, ensuring alignment with future operationalization constraints on [SonarCloud](https://sonarcloud.io), [SonarQube](https://www.sonarsource.com/products/sonarqube/), and [SonarLint](https://www.sonarsource.com/products/sonarlint/).
* Coded, in plain Java, the [RoBERTA](https://huggingface.co/docs/transformers/model_doc/roberta) tokenizer and a [Logistic Regression](https://en.wikipedia.org/wiki/Logistic_regression) model, matching precisely the reference implementation in Python (Scikit-learn + Hugging Face), to run across all SonarSource products.
* Designed and implemented with Step Functions the AWS workload running SonarQube code tweaked by ML scientists to produce data to train their model on, scaling EC2 instances to scan up to hundreds of projects within 30 minutes, with secured and autonomous control for ML scientists.
* Analyzed the produced data, with Jupiter Notebooks, Pandas, and Seaborn, to assist ML scientists.

**Technical Assets**

AWS (CDK, EC2, Step Functions, S3, IAM, System Manager), Python3, Scikit-learn, Poetry, Jupiter, Numpy, Pandas, Seaborn, Scikit-learn, Hugging Face, Java 11, Bash, Makefile

## Application Architect & Cloud Platform Engineer

[SonarSource](https://www.sonarsource.com/company/about/) ▪ Annecy, France ▪ 2022 - 2023

* Provided design support and advice on application and cloud-based architecture to the 4 delivery squads of the [SonarCloud](https://sonarcloud.io) team (35 people).     
* Handled research projects, unfit for the team's delivery pace, and occasionally joined squads' sprints as a Cloud Platform Engineer.     

SonarCloud is [SAAS](https://en.wikipedia.org/wiki/Software_as_a_service) with 1.3B+ API requests and a million server-side jobs per week, with a 6TB-storage relational database.

[//]: # (content to have: )
[//]: # (* worked on SonarCloud)
[//]: # (* worked on the challenging problems that required expert work outside regular delivery pace)
[//]: # (* worked on hard/spiky/hairy/challenging/out of delivery yet critical topics)
[//]: # (* Provided design support and advice to 4 delivery squads during the specification phase of their tri-weekly sprints or during weekly Specification Review team meetings)
[//]: # (    * => achievement: Reviewed the design and provided feedback on an average of 12 specifications a month, either as a participant into the specification phase of squad sprints or during weekly specification review team meetings)
[//]: # (* Provided hands-on support, as a Cloud Platform Engineer, to the 4 SonarCloud delivery squads during sprints under high pressure)
[//]: # (    * => Joined delivery squads as hands-on Cloud Platform Engineer during sprints under high pressure  )
[//]: # (* Participated in SonarCloud community support, performing investigation and resolution on an average of 10 threads per month)

**Achievements**

* Reviewed Architecture design on up to 6 specifications a month, during weekly specification review team meetings or as participant in the specification phase of squads' sprints.
* Designed and coded the weekly CodeBuild job sanitizing 0.5 to multi-billion rows, TB-scale tables in a 6TB+ Postgresql snapshot, optimizing DDL and SQL queries to ensure reliable completion within the 8 hours timeout, secure customer data, and enable developers to work on production-like data.
* Researched and optimized SQL queries to clean orphan rows in a 3.5B rows table for a daily, reentrant, and interruptable job, running on the writer node in production with no impact to users.
* Participated in [SonarCloud](https://sonarcloud.io) community support and backlog processing, focusing on cloud-based Security risks and costly in time/arduous threads and issues.

**Technical Assets**

AWS (CDK, CodeBuild, Aurora, RDS, ECS, SNS, SQS, Step Functions, Lambda, VPC, API Gateway, ELB, WAF), Python3, Postgresql, SQL

[//]: # (TODO)
[//]: # (* find technologies and topics I worked on as a CPE &#40;look into Jira?&#41;)

## Application Architect

[SonarSource](https://www.sonarsource.com/company/about/) ▪ Annecy, France ▪ 2021 - 2022 

* Lead the modelling of [SonarCloud](https://sonarcloud.io) as domains, following [Domain-Driven Design](https://en.wikipedia.org/wiki/Domain-driven_design) (DDD) methodologies to ensure solid and future-proof boundaries and definitions.  
* Prepared the forthcoming refactoring of SonarCloud from a monolith, based on [SonarQube](https://www.sonarsource.com/products/sonarqube/) and 10 years-old code, padded with cloud-based additions, to a microservice-based architecture upheld by domain-specific squads.

[//]: # (* Contributed the most part of the model, as the only person dedicated to the project)
[//]: # (* Main contributor to the model, as the only dedicated personnel to the effort)
[//]: # (* Thoroughly followed Domain-Driven Design &#40;DDD&#41; methodologies to ensure solid and future-proof boundaries and definitions)
[//]: # (* Main contributor to the modelling of SonarCloud along well-defined Domain-Driven Design &#40;DDD&#41; domains to prepare its refactoring from a monolith based on SonarQube to a fully micro-service-based architecture.)

**Achievements**

* Formed a modelling task force of squad- and skill-representing members, organizing DDD training with an external vendor, and managing the collaborative work pace with workshops and asynchronous tools.
* Incrementally modeled [SonarCloud](https://sonarcloud.io) as 3 core and 9 other domains, building up a model with 1k+ events representing 100+ processes within the service.
* Evangelized the model to the 4 delivery squads, sharing modelling updates, organizing workshops, writing up a reference documentation on DDD, and publishing 20+ notes solving squads' modelling questions.
* Led a team restructure (in a Reverse Conway Manoeuvre) around the defined domains and achieved clearer, smaller-scoped, and better scaling responsibilities, as well as comprehensive work sharing and community support among squads.
[//]: # (* Conducted book review meetings ... to ensure a common knowledge base on monolith refactoring technics and pitfalls across the team)

**Assets**

Domain Driven Design, Event Storming

## Cross-Teams Senior Software Engineer

[SonarSource](https://www.sonarsource.com/company/about/) ▪ Annecy, France ▪ 2020-2021

[//]: # (* Software Engineering excellence, advocacy and evangelism)
[//]: # (* Promote sustainable design and architecture in all products within the SonarSource portfolio)
[//]: # (* cross-team, )
[//]: # (* work on hard topics and researches unfit with the critical path of delivery / unfit to be tackled by team as part of delivery)

[//]: # (Achievements)
[//]: # (* Asynchronous indexing)
[//]: # (* JWT token revocation)
[//]: # (* database schema and data refactoring &#40;replacing integer IDs with UUIDs in million+ rows tables on 4 DBMS in 2 versions each&#41;)

[//]: # (I would like to announce that Sébastien is going to move out of the SonarQube team and take a new position as a Software Engineer, outside of product development teams.  Sébastien will work with Simon to achieve engineering excellence and promote sustainable design and architecture in our products)
[//]: # (Being a softare engineer outside of product development teams, in other words out of the critical path of product delivery, Sébastien will bring different perspectives to help the teams to achieve their missions. )
[//]: # (His development expertise will be at the service of the teams to:)
[//]: # (    Troubleshoot bugs, vulnerabilities and production incidents)
[//]: # (    Advise the teams on deep technical topics or design questions)
[//]: # (    Recommend best-practices)
[//]: # (    Train developers to existing or new technologies)
[//]: # (    Promote architecture and design changes)
[//]: # (    Implement POCs)
[//]: # (    Be onboarded in sprints by teams when strong technical skills are required)
[//]: # (    Share engineering knowledge among the different teams)

[//]: # (Promoted to Software Engineer outside of product teams to lead projects and research unfit for the critical path of delivery and/or crossing team boundaries.    )

* Lead projects and research unfit for the critical path of product delivery and/or crossing team boundaries.    
* Seconded the CTO in achieving engineering excellence and promoting sustainable design and architecture.   
* Delivered Proof-of-Concepts and research for product teams ahead of feature development, engineering consultations and design support to developer squads on demand, and company-wide expertise on relational databases, Elasticsearch and OpenSearch.  

**Achievements**

* Prescribed the company's policy for Artifacts Management, directed the teams' Release Software Engineers to modify CI/CD toolchains, and achieve consistent and secure management of software artifacts.
* Formed the Release Engineering Team at SonarSource (a support team bringing common tooling around CI/CD), contributing as the initial leader, and as an individual contributor to the Gradle, Maven, Bash scripting, and CI/CD codebase.
* Fixed and optimized search and indexing Elasticsearch requests, redesigned indices and requests to accommodate breaking changes from version upgrades, for both [SonarCloud](https://sonarcloud.io) and [SonarQube](https://www.sonarsource.com/products/sonarqube/).
* Concluded on the impact of the 2021 Elastic license change on SonarSource products, collaborating with the Legal Team.
* Designed and prototyped asynchronous indexing of data into Elasticsearch, achieving reduction of [SonarQube](https://www.sonarsource.com/products/sonarqube/) upgrade downtime from hours, linearly increasing with data size, to constant time under 30 minutes, and similarly achieving constant and under 1 hour Time To Recovery on SonarCloud.
* Researched and prescribed the solution to ensure JWT tokens expiry on [SonarCloud](https://sonarcloud.io), fixing Session Hijacking risks, and enabling targeted or global revocation in case of Security incident.

[//]: # (*  )
[//]: # (*  )
[//]: # (* Researched solutions to breaking changes caused by the upgrade Elasticsearch 4 indices &#40;ES&#41; on SonarQube instances with up to dozens of GB, achieving smooth upgrade thanks to the design and implementation of an asynchronous data indexing based on SonarQube's Compute Engine.  )
[//]: # (* Concluded on the impacts on Sonarqube of the Elastic licence change in 2021, collaborating with the Legal team, and provided expert support to the SonarCloud team during their migration from Elasticsearch to OpenSearch.)
[//]: # ()
[//]: # (* Topics included Elasticsearch &#40;ES&#41; upgrades, Asynchronous indexing into ES, Security Token storage and management)
[//]: # (* )
[//]: # (* Elastic search, license change impact, and major version upgrade)

**Technical Assets**

Elasticsearch, OpenSearch, Maven, Gradle, Bash, GitHub actions, Cirrus CI, Travis, Postgresql, SQL, MyBatis

## Backend Software Engineer 

[SonarSource](https://www.sonarsource.com/company/about/) ▪ Annecy area, France ▪ 2015 - 2020

[//]: # (Operated as a Backend Developer in the [SonarQube]&#40;https://www.sonarsource.com/products/sonarqube/&#41; team &#40;which grew from 3 to 15 members&#41;, )
[//]: # (during the startup and growth phase of the company, while cooperating directly with founding partners of SonarSource.   )
[//]: # (Directed the design, implementation, optimization, and troubleshooting of a multiprocess software made of a Java-based Webserver, )
[//]: # (a Java-based task processor, and embedded Elasticsearch, running on premises with deployments of all scales and supporting 4 different DBMS vendors.)

* Operated as a Backend Developer on [SonarQube](https://www.sonarsource.com/products/sonarqube/), the founding product of SonarSource, researching, designing, 
implementing, optimizing, and troubleshooting new features and improvements during the startup and growth phases of the business.   
* Engaged in development of webservice APIs, server-side task processing, Java-based clients, relational database, and internal hosting observability 
as well as production support, software security, engineering best practices, software build, open source publication, and hiring.

SonarQube is a Java-based server with clients for different build systems and CI/CD environments.  
The server includes a Webserver, a task processor, embedded Elasticsearch, and supports 4 DBMS vendors.  
On-premises deployments range from a few MB to hundreds of GB and handle a few to thousands of users.

[//]: # (************* COVERED *************)
[//]: # (&#40;which grew from 5, including the CTO, to 25 members&#41;, )
[//]: # (during the startup and growth phase of the business.   )
[//]: # (and while cooperating directly with founding partners of SonarSource.)
[//]: # (design, implementation, optimization, and troubleshooting)
[//]: # (developing new features, from research and design, to implementation, troubleshooting and support, in collaboration with Product Owners, Frontend developers and Ops)
[//]: # (spanning from the clients and the server, to the build system and infrastructure for both internal and public demonstration deployment)
[//]: # (database, web APIs, process management, Compute Engine,)
[//]: # (RoR migration,)
[//]: # (replaced clients connecting to database by asynchronous task processor on the server-side, achieving easier deployment for customers and unmatched scale of deployments)
[//]: # (High availability with several instance running in a cluster and coordinating over Hazelcast)
[//]: # (easy and safe coding of frequent database migrations.)

[//]: # (************* NOT YET COVERED &#40;if ever?&#41; *************)
[//]: # (design the incremental startup process of the server, supporting human trigger DB migrations)
[//]: # (design Java code and build to produce binaries for open-source, multiple closed sources editions and internal cloud-based deployment from the same codebase and repository.)
[//]: # (Codebase supporting both on premises and cloud-based deployment for early versions of SonarCloud.)


**Achievements**

[//]: # (* Leveraged instrumental impacts toward the design and code of the core features and concepts still in active existent programs presently.)
[//]: # (* Designed and coded a generic task processor and the report processing task in [SonarQube]&#40;https://www.sonarsource.com/products/sonarqube/&#41;.)
* Designed and coded a generic task processor, a task framework and the task processing reports from clients, enabling the removal of the connections from clients to the database and achieving tenfold scalability improvement.
* Honed expertise in troubleshooting and fixing performance issues with both the JVM memory flow and SQL queries, achieving Out-Of-Memory-Error-free report processing and consistent and reliable performance regardless of report size and content.
* Developed the automatic lifecycle management of [SonarQube](https://www.sonarsource.com/products/sonarqube/) instances working together as a cluster, over a Hazelcast network, to achieve high availability.
* Replaced a legacy, RoR-based database migration solution with a custom Java-based, SQL-free framework ensuring transparent support of and automated testing on 4 different DBMS, as well as consistent and performant behavior across versions and developers.
* Contributed to the growth of the development team, adding 5 people, as first hiring manager, screening resumes and conducting first and technical interviews.
* Invented and implemented [public-git-sync](https://github.com/lesaint/public-git-sync), the utility synchronizing several SonarSource private repositories (with both open and closed source code) with their open source counterpart, providing automated creation of clean and consistent Git history and content, with branches and tags support.

[//]: # (* RoR migration, adding Elasticsearch, cutting client connection to the database by adding an asynchronous task processor, cluster support, on premises + cloud based deployment)

[//]: # (* Operated as a Backend Developer on SonarQube &#40;SQ&#41; for five years while cooperating closely with founding partners of organization.)
[//]: # (* Leveraged instrumental impacts toward the design and code of the core features and concepts still in active existent programs presently.)
[//]: # (* Directed the design, implementation and optimization on a multiprocess software made of a Java-based Webserver, a Java-based task processor, and embedded Elasticsearch.)
[//]: # (* Designed and coded a generic task processor and the report processing task in SonarQube.)
[//]: # (* Honed expertise in troubleshooting and fixing performance issues with both the JVM and the database to ameliorate issues of all sizes on four various DBMS.)
[//]: # (* Completed memory flow optimization on the JVM along with database design and SQL optimizations on four DBMS targeting SQ instances of all sizes, including schema and data migrations.)
[//]: # (* TODO: hiring)

**Technical Assets**

Java 1.4 to 8, Maven, Gradle, MyBatis, Elasticsearch, Hazelcast, Bash, Jenkins, Postgresql, Mysql, MariaDB, Oracle, SQL Server, Git, Github, Jira

## Senior Developer

[Ekino](https://www.ekino.fr/) ▪ Paris, France ▪ 2014 - 2015

**Technical Assets**

Java 7, Spring Core/Mvc/Batch, MyBatis, MySQL, LiquiBase, Puppet, Capistrano, Logstash, Graylog2, RabbitMQ, Guava, Mockito, TestNG, Maven, Git, Jenkins, Tomcat, Apache, Linux, bash

**Achievements**

* Developed an innovative digital safe solution of the French postal office called Digiposte.
* Stewarded technical revamp from PHP to JAVA along with deep spring MVC customization, Thymeleaf integration, and SQL optimization.
* Tailored asynchronous processes along with Puppet/capistrano configuration in line with corporate specifications.

## Senior Developer / Technical Supervisor

[Fullsix](https://www.linkedin.com/company/fullsix-groupe/) ▪ Paris, France ▪ 2010 - 2014

**Technical Assets**

Java 7, Spring, GraniteDS, Oracle, CXF, JMS, ActiveMQ, LiquiBase, Guava, Mockito, TestNG, Maven, Git, Tomcat, Apache, Linux, Jenkins, Sonar, bash

**Achievements**

* Conceptualized and implemented SFR's Flex application for customer service and shops, including full integration and automation of platform.
* Facilitated software development lifecycle to streamline sales; managed continuous integration, quality assurance, source control, and release management.
* Oversaw technical support, incident investigations, and solutions design to enhance client experience.
* Conducted user requirements analysis and feasibility research to maximize scalability. 
* Launched and engineered a bespoke online store which serviced a diverse user base.
* Appointed two consecutive years to a four-person team of experts forming the on-call Support Level 3 for all web-based applications of SFR (2nd telco-company in France)

## Developer

Ginerativ ▪ Paris, France ▪ 2004 - 2010

**Technical Assets**

Java 5, EJB3, Oracle, PL/SQL, JDBC, XML, JAX-WS, Struts, JSP, Maven, multi-threading, Swing, SVN, JBoss, Apache

**Achievements**

* Created corporate website, Contracts Decision Automation System (DAS), and corresponding web services.
* Successfully directed off-shore applications development projects in Tunisia.
* Led user research and feasibility studies which contributed to design, development, and maintenance activities.

# Presentations

* (2021) Organized and prepared the internal presentation at SonarSource by engineers from [Malt](https://www.malt.fr/) sharing their experience: 8 years searching for the best observability stack
* (2017) Internal presentation at SonarSource: Do you know Climbing?
* (2016) Internal presentation at SonarSource: Functional Programing in Java with Guava 12's FluentIterable and Optional 
* (2015) Devoxx France – hands-on lab - Compile-time annotation processing: @Nailed("it")

# Education

* Master of Engineering in Computer Software Development ▪ ESIEA ▪ Paris, France
* Bachelor of Science in Computer Software Development (First Class Honours) ▪ Anglia Polytechnic University (APU) ▪ Chelmsford, UK
* High School Graduate with Mathematics, Biology, and Technical Majors ▪ Notre Dame la Riche ▪ Tours, France

# Certifications
 	
* AWS Certified Solutions Architect – Associate	
* AWS Certified Solutions Architect – Practitioner 

# Interests

* I climb twice a week indoors (boulder and lead) and make the best of mountain outdoors: alpine and Nordic skying in the winter, running, hiking, climbing, and swimming in lakes the rest of the year.
* I set up and maintain my home data protection strategy with rsync, Bash and Python, achieving full redundancy (local online and offline, remote online) and encryption across devices in the household. Recovered with no impact from home breaking in 2021.
* I enjoy sharing with my family outdoor activities, my collection of over 500 European comics and mangas, video games, movies, and my eclectic music taste.
