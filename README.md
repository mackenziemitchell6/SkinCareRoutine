# SkinCareRoutine

By Mackenzie Mitchell

## Overview

The goal of this project is to create a recommender system to recommend a set of skincare products (or a skincare routine) to a new user based on their skin type, skin problems, and the types of products they're looking for. Using data on products and reviews scraped from SkinStore.com, I created a recommender system using the surprise package in Python. 

![TargetDistplots](https://github.com/mackenziemitchell6/SkinCareRoutine/blob/master/Visuals/VennDiagram_AllBrands.png "All Brand Distribution")

## Obtaining Data
Data scraped using BeautifulSoup from:
https://www.skinstore.com.

In order to get data on all skincare products on the website, I scraped multiple landing product pages such as the product pages for product types such as cleanser, exfoliator, or toner and the product pages for specific skin concerns and skin types such as dry, oil, or normal/combination. From this I obtained the product names, prices, and the product urls and I could then navigate to each individual product page to get the review and rating data. 

By first scraping the different product pages, I was able to join all of these data frames and create categorical variables for each of the product types and skin types. This will later help me to further personalize recommendations. 

## Exploratory Data Analysis (EDA)

The dataset contained:
-  1,700 skincare products
-  102 brands
- ~3,300 reviews
- ~1,400 users

#### First we take a look at the distribution of prices:
![PriceDistribution](https://github.com/mackenziemitchell6/SkinCareRoutine/blob/master/Visuals/AllPricesDistribution.png "All Prices Distribution")

#### Next we take a look at the distribution of ratings:
![RatingDistribution](https://github.com/mackenziemitchell6/SkinCareRoutine/blob/master/Visuals/AllRatingsDistribution.png "All Ratings Distribution")

#### Taking a look at the distribution of product types:
![TypeDistribution](https://github.com/mackenziemitchell6/SkinCareRoutine/blob/master/Visuals/allDataTypesHistogram.png "All Product Types Distribution")

#### Taking a look at the distribution of skin types/problems:
![TypeDistribution](https://github.com/mackenziemitchell6/SkinCareRoutine/blob/master/Visuals/allDataProblemsHistogram.png "All Skin Types/Problems Distribution")

### Performing exploratory data analysis using Natural Language Processing of the review content allows us to get a sense for and establish the integrety of our ratings.

#### Observing the content sentiment of each review:
We can see that there are some low ratings that have abnormally high sentiment, and there are also high ratings that have abnormally low sentiment. However, the pattern seems to be roughly as expected.
![ContentSent](https://github.com/mackenziemitchell6/SkinCareRoutine/blob/master/Visuals/RatingSentimentPlot.png "Content Sent")

## Modeling
After trying many different models (KNN Basic, KNN Baseline, KNN with Means) with different parameters ({metric: pearson, cosine, pearson baseline},{user_based: True, False}, as well as SVD with grid search and NMF with grid search, the model with the lowest RMSE was a KNN Baseline model with the pearson baseline metric and item based filtering. 
  This resulted in an RMSE of 0.9645. 
