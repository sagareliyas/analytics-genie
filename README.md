# analytics-genie seytup
Create an azure account
Create a storage account and a container


# Logic app steps
1. Go to logic app designer
2. Start with creating a new step
3. From azure blob storage choose trigger 'when a blob is     added or modified'
4. Choose the storage account and container from the listed options
5. Initialize variables blob_data(String), var_audio_sas_url(String), var_trans_content(String), final_data(String), sentiment_analysis_data(String), speaker1_text(String), speaker2_text(String)
6. Choose Create SAS URI by path from Azure blob storage, choose the account name and add Blob path as 'List of Files Path'
7. Choose variable operation 'Append to string variable' and append 'Web Url' to variable 'var_audio_sas_url' from the response
8. Append blob data to the variable blob_data for saving to database with 'id' as 'List of Files Id', 'name' as 'List of Files DisplayName', url as 'var_audio_sas_url'
9. Create an HTTP Request with Method POST as next step for getting the transcription results. 
10. From the keys and endpoints section in Cognitive Service -> speech service copy the first portion of endpoint url and append with api url '/speechtotext/v3.0/transcriptions'
eg: https://centralus.api.cognitive.microsoft.com/speechtotext/v3.0/transcriptions , Headers with 'Ocp-Apim-Subscription-Key'. and body with 
{
  "contentUrls": [
    @{variables('var_audio_sas_url')}
  ],
  "displayName": "audiofiles",
  "locale": "en-US",
  "properties": {
    "diarizationEnabled": true,
    "profanityFilterMode": "Masked",
    "punctuationMode": "DictatedAndAutomatic",
    "wordLevelTimestampsEnabled": false
  }
}
11. Copy the result and give it as sample payload in Data operations -> Parse Json and  generate schema
12. Append to string variable 'var_trans_content' with dynamic value 'properties.status'
13. In the next step From Control Actions choose 'Until' with statement 'var_trans_content' is equal to 'Succeeded' 
14. Add a Delay of 1 minute
15. Trigger an HTTP Request with Method GET, in URL give dynamic generated variable 'self' with headers given before
16. Parse the json response generated from the previous request as before 
17. Append the dynamic data 'status' to variable 'var_trans_content'
18. For getting batch transcription files triger another HTTP GET request with dynamic url 'self' and add '/files' at the end of the url, key as headers passed before.
19. Parse the jscon response with content as dynamic variable 'Body'. Also copy the response of previous request as sample payload as done before.
20. Inside the foreach loop add dynamic variable 'values' and add Condition from Control Statement as dynamic variable 'kind' is equal to 'Transcription'
21. In the True Section add another HTTP GET REquest with url as dynamic variable 'contnetUrl' and headers as before
22. Parse Json with 'Body' and Schema as before.
23. Add another HTTP 'POST' request to our azure function in the azure app 'analyticdata' in the code.
the url is 'https://analyticsgenieapp.azurewebsites.net/api/analyticdata' and in the Body add dynamic variable 'Body'
24. Parse Json with body and sample payload generated with previous response.
25. Append the parsed 'Body' to string varible 'final_data'
26. Append parsed first 'text' to 'speaker1_text'
27. Append the parsed second 'text' to 'speaker2_text'
28. Pass the speaker1_text and speaker2_text for sentimental analysis.
Choose 'sentimental analysis v3' from actions 'Cognitive Services'
Add documents id-1 as dynamic generated variable 'createdDateTime' or any other unique value and document text-1 as 'speaker1_text'
Click on Add new item button and add another unique id which may be next 'createdDateTime' from parsed results and speaker2_text as text.
29. Append the results to string variable 'sentiment_analysis_data' with value dynamically genrated 'documents'
30. All these last 9 steps come under 'True' section of conditon inside the for each loop
31. Outside all add data to database by choosing Sql Server and action as 'Insert row(v2)'. add connection name, Authentication_type as 'SQL Server Authentication'


