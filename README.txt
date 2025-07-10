***DISCLAIMER AI was used during this project for front end and structure, I mainly focused on the logic as it is intended for my own personal learning***

This is meant as a general guide on farm health at a glance:

### How to use ###
I have a website up at https://agrihealth.onrender.com/ this is also available as an api on RapidAPi: https://rapidapi.com/samsewell95/api/agribusiness-farm-health-calculator/playground/apiendpoint_b436f5e2-ab7b-4abc-9e92-1147be6a650b

If you wish to run locally on your own device to test it out use this command in cmd: uvicorn main:app --reload (just make sure the directory is pointing to where the main.py file is)

required packages are also detailed in requirements.txt 

Identified constraints / Future Improvements - 

- Rainfall is only represented as an average, the main risk in agriculture is rain variability. Which needs to be represented as it is a large component of agriculture. 

- Enterprises conducted on farm should also have an impact on risk scoring, as different metrics would be weighted differently. e.g. Irrigation is less important for Beef than it is for vegetables or broadacre. 

- Geographical location is also not considered, while rainfall can indicate some limited climate data it would be better to have an idea of temperatures and soil type. However this is a infinitely expanding issue that goes well beyond the scope of this project. 

- It would also be beneficial to be able to test specifc sub sections, e.g financial health only or productivty only. At the moment the user has to input in all datafields for a result to be generated. 



