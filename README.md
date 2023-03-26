# [Python + Google Cloud Platform (Google Cloud Storage, Bigquery, Cloud Function, Compute Engine)] VNStock Daily Data

## Introduction

Bài toán: Get data on Vietnam's stock market to base on data to make decisions in buying and selling stocks.

Yêu cầu:

Snapshot of all stock data from 01/02/2010 to the current time and save in Google Cloud Storage and write to Bigquery.
Automating the daily data pipeline will be updated every 4pm and saved to GCS & Imported into Bigquery.

## How to use

Step 1 : Clone my project

`git clone https://github.com/thangnh1/Vnstock-Data-GCP`

Step 2 : Open in editor tool, run command in terminal

`pip install -r requirements.txt`

Step 3 : Run file `get_data.py`

`python get_data.py`

After running file `get_data.py`, file `data.csv` contains all stock data from past to present time

Step 4 : Load data to GCS and Bigquery

At Google Console, create new project, activate APIs Service : Bigquery, Cloud Storage, Compute Engine, Cloud Function.
<p align="center">
  <img src="demo/video_1_1.gif" width="200">
  <img src="demo/video_1_2.gif" width="200">
  <img src="demo/video_1_4.gif" width="200">
  <img src="demo/video_2_1.gif" width="200"><br/>
</p>


Then search `IAM & Admin`. In IAM & Admin NavMenu, choose Service Accounts

<br />
<p align="center">
  <img src="demo/demo_iam.png"><br />
  <i>NavMenu IAM & Admin</i>
</p>

Click `CREATE SERVICE ACCOUNT` and fill info

<br />
<p align="center">
  <img src="demo/demo_sv_acc.png"><br />
  <i>Create service account &</i><br /><br />
  <img src="demo/demo_sv_acc_1.png"><br /><br />
  <img src="demo/demo_sv_acc_2.png"><br /><br />
  <img src="demo/demo_sv_acc_3.png"><br />
  <i>Fill Infomatiton account</i><br /><br />
</p>

Now, your service account is created!

<br />
<p align="center">
  <img src="demo/demo_sv_acc_4.png"><br />
  <i>List Service Account & Detail</i>
</p>

Select the newly created account, switch to the `Keys` > `Add key` > `Create new key`

<br />
<p align="center">
  <img src="demo/demo_sv_acc_5.png"><br />
  <i>Create key</i>
</p>

Choose `JSON Type` and Create, a JSON file containing your credentials will be downloaded to the local server

<br />
<p align="center">
  <img src="demo/demo_sv_acc_6.png"><br /><br />
  <img src="demo/demo_sv_acc_7.png"><br /><br />
  <img src="demo/demo_sv_acc_8.png"><br />
  <i>JSON file key</i>
</p>

Back to Editor, open `push_data.py`, edit variable value, then run command `python push_data.py` <br />
Check GCS and Bigquery in Google Console.

## Demo

