# JobCruncher


<p align="center">
<img src="https://user-images.githubusercontent.com/52947925/194793741-d5de162e-f915-4187-b463-24300f0ab215.gif">
</p> 





![GitHub License](https://img.shields.io/github/license/SE24Fall/Job-Analyzer)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
![GitHub Issues](https://img.shields.io/github/issues/Sankar16/Job-Analyzer)
![GitHub Issues closed](https://img.shields.io/github/issues-closed/SE24Fall/Job-Analyzer)
![GitHub contributors](https://img.shields.io/github/contributors/SE24Fall/Job-Analyzer)
![GitHub repo size](https://img.shields.io/github/repo-size/Sankar16/Job-Analyzer)
![GitHub Pull Requests](https://img.shields.io/github/issues-pr/Sankar16/Job-Analyzer)
![GitHub Pull Requests Closed](https://img.shields.io/github/issues-pr-closed/Sankar16/Job-Analyzer)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/TejasPrabhu/Job-Analyzer/unit-tests)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14027279.svg)](https://doi.org/10.5281/zenodo.14027279)
[![flake8](https://github.com/Sankar16/Job-Analyzer/actions/workflows/flake8.yaml/badge.svg)](https://github.com/Sankar16/Job-Analyzer/actions/workflows/flake8.yaml)
[![pyflakes](https://github.com/Sankar16/Job-Analyzer/actions/workflows/pyflakes.yaml/badge.svg)](https://github.com/Sankar16/Job-Analyzer/actions/workflows/pyflakes.yaml)
[![autopep8](https://github.com/Sankar16/Job-Analyzer/actions/workflows/autopep8.yaml/badge.svg)](https://github.com/Sankar16/Job-Analyzer/actions/workflows/autopep8.yaml)
[![CodeQL Advanced](https://github.com/Sankar16/Job-Analyzer/actions/workflows/codeql.yml/badge.svg)](https://github.com/Sankar16/Job-Analyzer/actions/workflows/codeql.yml)
[![Code Coverage](https://github.com/Sankar16/Job-Analyzer/actions/workflows/code_coverage.yml/badge.svg)](https://github.com/Sankar16/Job-Analyzer/actions/workflows/code_coverage.yml)

## Group 60
Juggling multiple assignments, quizzes, projects, presentations, and clutching the deadlines every week? Feel like you have no time to watch your favorite series or sports team play let alone search for job posting on a day-to-day basis? Here comes JobCruncher.

JobCruncher is built for those with packed schedules, balancing studies, projects, and personal interests. It simplifies job searching by providing an easy-to-use, streamlined platform for finding the best-matched roles in less time. With a lightweight, user-friendly interface, JobCruncher lets users have a secured platform, modify resume, bookmark job postings and filter job postings according to title, location, company, skills, and job type, giving you the freedom to focus on life while we handle the search. 

So, leave the tedious and monotonous task of looking up the job postings to our JobCruncher that not only provides the jobs posted every day but helps to filter out the results based on your liking.

## PHASE:02

# So why use JobCruncher instead?

## Project Video
https://github.com/user-attachments/assets/3a5857ee-497e-4185-a770-513f36ab3f61

## Project Video
https://www.youtube.com/watch?v=H823ocClZ-k

Unlike many other job portals, JobCruncher is a simple, lightweight, online tool that helps users get clear information about the jobs posted on LinkedIn and further help the user finetune the results.

Further, it helps to provide the user insights about the job postings and as the scraper is executed every day, the user is always provided with the most recent job postings.

With the new enhancements for resume Analysis to find your ATS score, Getting notified about new job postings which are tailored according to your need and enhanced security with 2FA authentication, job cruncher has become more robust and engaging than ever before.

# Deployment and Scalability
![arch](https://user-images.githubusercontent.com/57044378/205757699-815515cd-a07b-4d64-8ca5-f61f9e82c080.jpg)
The Job Analyzer applocation can be deployed on any cloud service provider like AWS, GCP, Azure using docker image created by docker file. We have created deployment service and route yaml files for kubernetes to access the application publically. As the number of users increases from 100, 1000, 10000.... we need to increase the number of container instances. As we have Global Traffic Manager (GTM) to load balance multiple user requests to different datacenters through Local Traffic Manager (LTM) using Ngnix. In the cloud we also have a HA proxy/services to distribute each request to a container which is having the least load to serve the request. In the backend we have mongodb deployed on different datacenters which will asynchronously replicate the data using multileader architecture. By using this architecture we can accomodate every user request without affecting the performance of our application. We will be using A:A deployments to increase the availability of our application.

# Installation

Check [INSTALL.md](https://github.com/SE24Fall/Job-Analyzer/blob/main/INSTALL.md) for installation instructions for Python, VS Code and MongoDB

# To get started with project
* Clone the repo
   ```
    git clone https://github.com/SE24Fall/Job-Analyzer.git
  
  ```
* Setup virtual environment
  ```
  pip install virtualenv
  cd Job-Analyzer
  virtualenv env
  .\env\Scripts\activate.bat
  ```
* Install required libraries by 
  
  ```
    pip install -r requirements.txt
  
  ```

* After running command 'flask --app src.app run', in the directory containing src directory you are good to go
  
  ```
    flask --app src.app run

  ```
  
# Application Preview:

### Homepage
![image](https://github.com/user-attachments/assets/f0f31843-3bd6-4f89-9485-686f66247c0c)

### Search criteria
![image](https://github.com/user-attachments/assets/5097927c-ec9e-42b2-8dd2-16b687c291fa)

### Job listings
![image](https://github.com/user-attachments/assets/a8888418-8529-4bac-a8cd-5df118c6d605)

### Edit profile
![image](https://github.com/user-attachments/assets/ee06b892-783c-488d-b40d-cb62e0461f37)

### Two-factor Authentication
<img width="1512" alt="Screenshot 2024-11-26 at 7 09 19 PM" src="https://github.com/user-attachments/assets/6cb71490-f741-4ed6-a261-b41419128c7e">

### Resume Analyzer
<img width="1512" alt="Screenshot 2024-11-26 at 7 10 48 PM" src="https://github.com/user-attachments/assets/71cd9001-62fc-48d8-8799-061d135838b0">

### Push Notifications 
<img width="1512" alt="Screenshot 2024-11-26 at 7 17 35 PM" src="https://github.com/user-attachments/assets/82e33c29-2237-4fff-8477-566433f1822e">


# Tech Stack used for the development of this project
 
 <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="python" width="20" height="20"/> Python </br>
 <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mongodb/mongodb-original.svg" alt="mongo" width="20" height="20"/> MongoDB </br>
 <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-plain.svg" alt="flask" width="20" height="20"> Flask </br>
 <img src="https://user-images.githubusercontent.com/52947925/194781771-ccf8e200-6b64-41ae-9eac-65f73367f377.svg" alt="selenium" width="20" height="20"> Selenium </br>
 <img src="https://user-images.githubusercontent.com/52947925/194781751-eb3701f1-3770-45d0-824d-721e73711111.svg" alt="pytest" width="20" height="20"> Pytest </br> 

## Project documentation

The `docs` folder incorporates all necessary documents and documentation in our project.

## Code Coverage

[![codecov](https://codecov.io/gh/TejasPrabhu/Job-Analyzer/branch/main/graph/badge.svg)](https://codecov.io/gh/TejasPrabhu/Job-Analyzer)


| Files | Coverage    |
| :---:   | :---: |
|src/scraper.py      |	61.34%  |
|test/test_flask.py  |	100.00% |
|src/app.py          |	100.00% |
 

## Future Scope:
   As the job market grows exponentially every year, the JobCruncher tool has to keep up with this pace and hence has to shed many overheads induced in the current process.
   
### Phase 3 FUTURE ROADMAP:

  1. **Containerization with Docker:** Use Docker to containerize the JobCruncher application, ensuring consistency across development, testing, and production environments. This simplifies deployment and dependency management, reducing environment-related issues.
  2. **Recruiter Portal:** Introduce a portal for recruiters to post jobs, manage applications, and interact with candidates. This facilitates direct communication between job seekers and recruiters, streamlining the hiring process within JobCruncher.
  3. **Advanced Data Scraping Mechanisms:** Implement sophisticated scraping techniques to aggregate job postings from various online sources in real-time. This expands the job database, offering users more comprehensive and up-to-date job listings.
  4. **Orchestrated Deployment with Kubernetes:** Utilize Kubernetes to automate deployment, scaling, and management of the containerized application. This allows JobCruncher to efficiently handle increasing user loads with robust load balancing and self-healing capabilities.
  5. **Advanced Job Matching Algorithm:** Enhance the job recommendation system with machine learning algorithms that better understand user preferences and skills. This delivers more accurate and relevant job suggestions, improving user satisfaction.


## Contributors
Thanks goes to these wonderful people. 
<table>
  <tr>
    <td align="center"><a href="https://github.com/apurv-choudhari"><img src="https://avatars.githubusercontent.com/u/81951099?s=400&v=4" width="100px;" alt=""/><br/><sub><b>Apurv Choudhari</b></sub></a></td>
    <td align="center"><a href="https://github.com/Prabhudatta3004"><img src="https://avatars.githubusercontent.com/u/75059607?s=400&v=4" width="100px;" alt=""/><br/><sub><b>Prabhudatta Mishra</b></sub></a></td>
    <td align="center"><a href="https://github.com/Sankar16"><img src="https://avatars.githubusercontent.com/u/179175525?s=400&v=4" width="100px;" alt=""/><br/><sub><b>Sankar Raghuthaman</b></sub></a></td>
  </tr>
</table>

<table>
  <tr>
    <td align="center"><a href="https://github.com/abivis2k"><img src="https://avatars.githubusercontent.com/u/81951099?s=400&v=4" width="100px;" alt=""/><br/><sub><b>Abishek Viswanath Pittamandalam</b></sub></a></td>
    <td align="center"><a href="https://github.com/ashwinchelsea14"><img src="https://avatars.githubusercontent.com/u/75059607?s=400&v=4" width="100px;" alt=""/><br/><sub><b>Ashwinkumar Manickam Vaithiyanathan</b></sub></a></td>
    <td align="center"><a href="https://github.com/ishwarya0103"><img src="https://avatars.githubusercontent.com/u/179175525?s=400&v=4" width="100px;" alt=""/><br/><sub><b>Ishwarya Anandakrishnan</b></sub></a></td>
  </tr>
</table>
