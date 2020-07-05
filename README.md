# crawler-for-job-application
This project is a small task for job application. The goal is to crawl the shower door products on *www.build.com*. The praogram is implemented with **Selenium** due to the JS-rendered content on the website

## Progress
- [x] prices, product names, ratings of the products
- [ ] "Dimensions and Measurements, Characteristics and Features, Warranty and Product Information" of the products. (**Failed on "Please varify you are a Human" anti-crawling mechanism**)

## Envs
```
python==3.7
pipenv=="*"
```

## Project setup
```
pipenv install Pipfile
```
### Scrape data
```
pipenv run scrape
#htlm is stored and named 'raw_html.html'
```
### Preprocess&ouput data
```
pipenv run preprocess
#output is named 'results.csv'
```

### Bugs
I failed on crawling the product page due to the "Please varify you are a Human" anti-crawling mechanism. I have added User Agent, language, plugins, cookies, etc. Still, I always got redirected to the Google Captcha verification page.

<p align="center"><img src="https://github.com/nicksome168/crawler-for-job-application/blob/master/src/fail.png"></p>

I have searched some workaround measures and found this website [Detecting Headles Chrome](https://intoli.com/blog/making-chrome-headless-undetectable/) teaching how to bypass the anti-crawler dedector. I have already passed most of them and left the "Hairline Feature" unchecked due to limited time. I am not sure if that's the cuase of the failure and futher work is needed.

<p align="center"><img src="https://github.com/nicksome168/crawler-for-job-application/blob/master/src/test.png"></p>