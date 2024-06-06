title: Resume 2
subtitle: Sébastien Lesaint - Senior Software Engineer & Application Architect
slug: sebastien_lesaint_resume_wip
status: hidden

[TOC]

[//]: # (# Professional Profile)

[//]: # ()
[//]: # (Goal-driven technical professional with an illustrated track record of innovation in high quality software development, complex systems modelling, cloud-based architecture, and backend programming for high-traffic website. 15 years expert in Java development and Python programming. Eager to learn and adopt new approaches and languages to fulfil requirements particular to unique contexts. Demonstrated expertise in technology management, including application server management and knowledge sharing. Conversant to industry trends and driving continuous improvement through the adoption of new tools and methodologies. Proven leader recognized for strong technical acumen, as well as dynamic problem-solving, communication, interpersonal, analytical, and decision-making skills.)

[//]: # ()
[//]: # (# Competencies)

[//]: # ()
[//]: # (* Technical Design Domain Driven Design ▪ Business Rules Analysis ▪ Research & Development ▪ Programming Open Source Mapping ▪ Quality Assurance Production Troubleshooting ▪ Stakeholder Engagement ▪ Performance Optimization &#40;SQL, CPU/Mem, Cross-Service&#41;)

# Career Summary

## Machine Learning Engineer

[SonarSource](https://www.sonarsource.com/company/about/) ▪ Annecy, France ▪ 2023 - 2024

Collaborated closely with SonarSource's Machine Learning (ML) scientists, providing integral support to 4 research initiatives, notably through the crafting of cloud-based and scaling solutions tailored to their requirements.

**Achievements**

* Effectively influenced the direction of 2 ML research studies, ensuring alignment with future operationalization constraints on SonarCloud, SonarQube, and SonarLint.
* Coded, in plain Java, the RoBERTA tokenizer and a Linear Regression model, matching precisely the reference implementation in Python (Scikit-learn), to run across all SonarSource products.
* Designed and implemented with Step Functions the AWS workload running SonarQube code tweaked by ML scientists to produce data to train their model on, scaling EC2 instances to scan up to thousands of projects within 30 minutes, with secured and autonomous control for ML scientists.
* Performed data analysis, with Jupiter Notebooks with Pandas and Seaborn of the produced data, to assist ML scientists.

**Technical Assets**

AWS (CDK, EC2, Step Functions, S3, System Manager), Python3, Scikit-learn, Poetry, Jupiter, Numpy, Pandas, Seaborn, Scikit-learn, Java 11, Bash, Makefile

## Application Architect & Cloud Platform Engineer

[SonarSource](https://www.sonarsource.com/company/about/) ▪ Annecy, France ▪ 2022 - 2023

Provided design support and advice on Application and Cloud-based Architecture to the 4 delivery squads of the SonarCloud team, autonomously handled projects unfit for delivery pace, and occasionally joined squads' sprints as Cloud Platform Engineer.  

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

* Reviewed Architecture design on up to 8 specifications a month, during weekly specification review team meetings or as participant in the specification phase of squads' sprints
* Designed and coded the weekly CodeBuild job sanitizing multiple XXXM rows tables in a XXXGb Postgresql snapshot, optimizing DDL and SQL queries to ultimately reliably complete within the 8 hours timeout
* TODO: Job to clean orphans
* Participated in SonarCloud community support, tackling arduous threads with long investigations

**Technical Assets**

AWS (CDK, CodeBuild, Aurora, ECS, SNS, SQS, Step Functions, Lambda), Python3, Postgresql, SQL

[//]: # (TODO)
[//]: # (* size of table &#40;rows and storage&#41;)
[//]: # (* size of postgresql dump)
[//]: # (* find technologies and topics I worked on as a CPE &#40;look into Jira?&#41;)
[//]: # (* techno and design of job to clean orphans )

## Application Architect

[SonarSource](https://www.sonarsource.com/company/about/) ▪ Annecy, France ▪ 2021 - 2022 

Lead the effort to model SonarCloud as domains, following Domain-Driven Design (DDD) methodologies to ensure solid and 
future-proof boundaries and definitions, to prepare for and support the refactoring of SonarCloud from a monolith, based 
on SonarQube and 10 years-old code padded with cloud-based additions, to a microservice-based architecture standing on domain-specific squads.

[//]: # (* Contributed the most part of the model, as the only person dedicated to the project)
[//]: # (* Main contributor to the model, as the only dedicated personnel to the effort)
[//]: # (* Thoroughly followed Domain-Driven Design &#40;DDD&#41; methodologies to ensure solid and future-proof boundaries and definitions)
[//]: # (* Main contributor to the modelling of SonarCloud along well-defined Domain-Driven Design &#40;DDD&#41; domains to prepare its refactoring from a monolith based on SonarQube to a fully micro-service-based architecture.)

**Achievements**

* Formed a modelling task force of team- and skill-representing members, organizing the training with an external vendor on DDD, and managing the collaborative work pace with workshops and asynchronous tools
* Incrementally modeled SonarCloud as 3 Core Domains and 9 additional domains, building up a model with 1k+ events representing 100+ processes within the service
* Evangelized the model to the 4 delivery squads, sharing modelling updates, organizing workshops, writing up a reference documentation on DDD, and publishing a diary with 20+ entries solving squads' modelling questions over the course of 6 months
* Led a team restructure (in a Reverse Conway Manoeuvre) around the defined domains and achieved clearer, smaller-scoped, and better scaling responsibilities, as well as comprehensive work sharing initiatives and community support among squads.

**Assets**

Domain Driven Design, Event Storming

## Cross-Teams Senior Software Engineer

[SonarSource](https://www.sonarsource.com/company/about/) ▪ Annecy, France ▪ 2020-2021

**Technical Assets**

MyBatis, Elasticsearch, Maven, Gradle, Github actions, Cirrus-ci, Postgresql

**Achievements**

* Determined engineering topics crossing product team boundaries (testing, CI/CD) to support Release Engineering Team at SonarSource: a support team bringing common tooling around CI/CD and responsible for consistent and secure management of technical artefacts.
* Delivered Proof-of-Concepts and research for product teams ahead of feature development. Topics included Elasticsearch (ES) upgrades, Asynchronous indexing into ES, Security Token storage and management
* Provided engineering consultations and design support to developer squads on demand.

## Backend Software Engineer on SonarQube

[SonarSource](https://www.sonarsource.com/company/about/) ▪ Annecy area, France ▪ 2020 - 2021

**Technical Assets**

Java 1.4 to 8, Maven, Gradle, MyBatis, Elasticsearch, Bash, Jenkins, Postgresql, Mysql, MariaDB, Oracle, SQL Server, Git, Github, Jira

**Achievements**

* Operated as a Backend Developer on SonarQube (SQ) for five years while cooperating closely with founding partners of organization.
* Leveraged instrumental impacts toward the design and code of the core features and concepts still in active existent programs presently.
* Directed the design, implementation and optimization on a multi-process software made of a Java-based Webserver, a Java-based task processor, and embedded Elasticsearch.
* Designed and coded a generic task processor and the report processing task in SonarQube.
* Honed expertise in troubleshooting and fixing performance issues with both the JVM and the database to ameliorate issues of all sizes on four various DBMS.
* Completed memory flow optimization on the JVM along with database design and SQL optimizations on four DBMS targeting SQ instances of all sizes, including schema and data migrations.

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

# Talks

* Devoxx FR 2015 – hands-on lab - Compile-time annotation processing: @Nailed("it")

# Education

* Master of Engineering in Computer Software Development ▪ ESIEA ▪ Paris, France
* Bachelor of Science in Computer Software Development (First Class Honours) ▪ Anglia Polytechnic University (APU) ▪ Chelmsford, UK
* High School Graduate with Mathematics, Biology, and Technical Majors ▪ Notre Dame la Riche ▪ Tours, France

# Certifications
 	
* AWS Certified Solutions Architect – Associate	
* AWS Certified Solutions Architect – Practitioner 

# Interests

Photography ▪ Editing ▪ Movies ▪ Comic Books ▪ Plays ▪ Video Games ▪ Boulder and Rock Climbing ▪ Hiking ▪ Nordic and Alpine Ski