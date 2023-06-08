<a name="readme-top"></a>

<br />
<div align="center">
  <a href="https://github.com/paverGulyaevich/recommender_3000/tree/master/project_app">
    <img src="https://github.com/paverGulyaevich/recommender_3000/blob/master/rec_bot_.png" alt="Logo" width='250' >
  </a>

<h3 align="center">Recommender 3000</h3>

  <p align="center">
    Content-Based Recommender System
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#objectives">Objectives</a></li>
        <li><a href="#project-files-description">Project Files Description</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#demo">Demo</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

Assume we created a simple social network for people, which allows them to send messages, read the feed and make posts. 

Every user on the platform can interact with the posts by viewing and putting likes on them. But we would like to make our service better and show our users the posts they might like the most.

All the users, posts and feed tabular data are stored in a database as follows:
* **user_data** table contains information about users:
  * age - Age of a user;
  * city - City of a user;
  * country - Country of a user;
  * exp_group - Experimental group;
  * gender - User's gender;
  * id - User's id;
  * os - Type of OS used by a user;
  * source - Source a user came to the platform from

* **post_text_df** table contains information about posts:
  * id - Unique post’s id;
  * text - Textual content of a post;
  * topic - Main topic of a post;


* **feed_data** tracks a user's interaction with posts:
  * timestamp - Time when a user interacted with a post;
  * user_id - User's id;
  * post_id - Post's id;
  * action - Type of action: view or like 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python](https://img.shields.io/badge/-Python-blue)](https://www.jetbrains.com/pycharm/)
* ![SQL](https://img.shields.io/badge/-SQL-orange)
* [![Pycharm](https://img.shields.io/badge/-PyCharm-brightgreen)](https://www.jetbrains.com/pycharm/)
* [![Kaggle](https://img.shields.io/badge/-Kaggle-informational)](https://www.kaggle.com/)
* [![FastApi](https://img.shields.io/badge/-FastApi-black)](https://fastapi.tiangolo.com/lo/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Objectives

- The main objective of this project was to build a web service that predicts and displays top-5 posts to a user in which he might be interested the most.
  To accomplish that Content-Based recommender system technique was implemented by means of machine learning.
- The idea was also to conduct a simulation of A/B test. For this purpose, all the users were divided into two groups (control and test) as well as two different ML models were trained to get predictions. The control group was exposed to a “weaker” model and the test group – to a “stronger” one.
- Additionally, the recommender system was integrated with a Telegram bot. 


<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Project Files Description
#### Executable Files:
* ***app.py*** - Runs our web service;
* ***recommender_bot.py*** - Runs the telegram bot with recommendations;
* ***my_models/catboost_control_tfidf.ipynb*** – A jupyter notebook where a model for the control group was trained;
* ***my_models/catboost_test_bertemb.ipynb*** – A jupyter notebook where a model for the test group was trained;
#### Output Files:
* ***catboost_model_tfidf*** – a trained model used for the control group;
* ***catboost_model_bertemb*** – A trained model used for the test group.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

1. Make sure you have [Python](https://www.python.org/) installed.
2. I recommend you use [Pycharm](https://www.jetbrains.com/pycharm/) as an interpreter.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/paverGulyaevich/recommender_3000.git
   ```
2. Open ***app.py*** and navigate to “project_app” folder by running the following command on the terminal:
   ```sh
   cd project_app
   ```
3. Run `uvicorn app:app –reload` command on the terminal to start the service.

4. Wait until the message *Service is up and running* appears.

5. To start the telegram bot execute ***recommender_bot.py***

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

1. Open the [bot](https://t.me/top5_posts_bot).

2. Follow the instructions on the screen.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Demo

<img align='center' src="https://github.com/paverGulyaevich/recommender_3000/blob/master/demo.gif" height='500' />

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

