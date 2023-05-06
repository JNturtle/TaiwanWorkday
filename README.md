# TaiwanWorkday
從「中華民國政府行政機關辦公日曆表」下載csv，然後檢查日期是否為臺灣工作天。
中華民國政府行政機關辦公日曆表 https://data.gov.tw/dataset/14718

isTaiwanWorkday(date)，輸出True為工作天，輸出False為非工作天。

date類型可為格式"%Y%m%d"的string，或是datetime類型。
