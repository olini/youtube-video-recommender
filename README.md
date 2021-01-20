# youtube-video-recommender

#### *Project based on the online course from Mario Filho, [Como Criar uma Solução Completa de Data Science](https://hotmart.com/product/como-criar-uma-solucao-completa-de-data-science)*

A YouTube video recommender solution, using machine learning to recommend videos on topics like machine learning, data science and kaggle. Deployed and hosted on [Heroku]()

This project consists on scraping videos from YouTube about certain keywords ('machine learning', 'data science' and 'kaggle'), process and label this data, determine features and create a machine learning solution to recommend new relevant videos on YouTube about these topics.
###### Observation: In this context, "relevant videos" are based on the labelling phase, the criteria used is better explained in the notebook.

### File structure:
* The notebook "youtube_video_recommender_notebook.ipynb" contains the whole process of data scrapping, data cleaning, labeling, creation of features, active learning and modeling.

* The folder "deploy/" contains all the files to run the flask web app and the docker container. The application is hosted on Heroku.
