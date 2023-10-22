# Technical Documentation


## Project description
This technical documentation serves as a guide for understanding and working with the API LAYER project.
APILayer is an API marketplace. APILayer is a provider of off-the-shelf, cloud-based API products built to help developers and businesses around the world operate quickly and effectively. 


## Prerequisites and dependencies

* _Pytest 7.4.0_ : This was used to run the test suite for the backend application
* _Pillow 9.5.0_ : This was used for validating images when an api is submitted


## Installation / Local Setup

please specify local setup of the application


## Test Setup
please specify how to run tests



## **Key Features Added** 

### 1.0 API SUBMISSION & LISTING:

Allows providers to submit APIs, which go through a review process before being listed on the platform.
User Sign Up: Simplified registration process with a password toggle feature.


#### Submission HTML Form

The submission form includes the following fields:

* API Name
* Short Description
* Documentation URL
* Long Description
* Logo URL
* Pricing Plans URL
* Response Example


#### Workflow

* Providers submit APIs, which are initially marked as "in review."
* Administrators are notified via email for new API submissions.
* Upon approval, the API status is updated to "live," and the data is copied to the API listings table.
* Approved APIs appear on the home page for users to access.

#### Database Structure for API Submissions and Listings
        
#### api_submissions table
       - id                     -> int
       - status_code            -> inherites from api_stats table
       - api_id                 -> stores the api_listing id
       - user_id                -> the provider id
       - api_name               -> holds the api name
       - short_description      -> holds the api short description
       - documentation_url      -> holds providers api doc url
       - long_description       -> holds the api long description
       - logo_url               -> holds the provider api logo
       - pricing_plan_url       -> holds the pricing url for the api
       - free_plan_is_available -> (boolean) denotes if api subcription is free or not
       - response_example       -> sample api response of the provider
       - version
       - changelog
       - created_at
       - service_name           -> added/created on api creation using the api_name

#### api_listing table
       - id                     -> int
       - status_code            -> inherites from api_stats table
       - api_id                 -> stores the api_listing id
       - api_submission_id      -> stores the api_submission id of a particular api
       - user_id                -> the provider id
       - api_name               -> holds the api name
       - short_description      -> holds the api short description
       - documentation_url      -> holds providers api doc url
       - long_description       -> holds the api long description
       - logo_url               -> holds the provider api logo
       - pricing_plan_url       -> holds the pricing url for the api
       - free_plan_is_available -> (boolean) denotes if api subcription is free or not
       - response_example       -> sample api response of the provider
       - version
       - changelog
       - created_at
       - service_name           -> added/created on api creation using the api_name


### API Submission & Listing API Endpoint
    
    
### Endpoint: /api/submissions

#### Overview
The API Submission & Listing functionality allows providers to submit APIs for review and subsequently list them on the platform. This section provides documentation for the /api/submissions endpoint.

#### Request Body
The request body should be in JSON format and contain the following fields:

- api_name (string): The name of the API.
- short_description (string): A brief description of the API.
- documentation_url (string): URL to the API documentation.
- long_description (string): A more detailed description of the API.
- logo_url (string): URL to the API logo.
- pricing_plans_url (string): URL to the pricing plans for the API.
- response_example (string): An example of the API response.

    

#### Example Request:

    POST /api/submissions
    Host: your-api.com
    Authorization: Bearer your-auth-token
    Content-Type: application/json
    
    {
        "api_name": "Sample API",
        "short_description": "A sample API for demonstration.",
        "documentation_url": "https://sample-api-docs.com",
        "long_description": "This API provides various endpoints for testing purposes.",
        "logo_url": "https://sample-api.com/logo.png",
        "pricing_plans_url": "https://sample-api.com/pricing",
        "response_example": "Sample response data here."
    }


#### Response
Upon successful submission, the API returns an HTTP status code 201 (Created) and a JSON response containing the following fields:

    HTTP/1.1 201 Created
    Content-Type: application/html
    
    {
        'apis': api_requests, 
        'provider': provider
    }




#### Error Responses

#### HTTP Status: 400 Bad Request
- If the request is missing required fields or contains invalid data, the API will respond with an error message.


    HTTP/1.1 400 Bad Request
    Content-Type: application/json
    
    {
        "error": "Invalid or missing data in the request."
    }

#### Usage Notes
      - Use proper authentication to access this endpoint.
      - Ensure that the request contains all required fields.
      - The submitted API will go through a review process before being listed on the platform. Administrators will be notified of new submissions.
      - Approved APIs will appear in the API listings for users to access.






### 2.0  USER SIGN UP: 




Simplified registration process with a password toggle feature.








Key Features : 
User Sign Up: Simplified registration process with a password toggle feature.
Navigation Bar: UI updates
Home Page: Displays prompt api APIs and provider-created APIs for users to explore.
Login and Zero State Page: Different user scenarios determine their landing page upon login.
Product Page: Shows details about an api selected by the user from the home page
Stylesheet Updates
Added Libraries: 
Pytest 7.4.0: This was used to run the test suite for the backend application
Pillow 9.5.0: This was used for validating images when an api is submitted






API Submissions and Listing


Overview
The API submission and listing process enables providers to offer their APIs to users. It includes a submission form where providers enter essential details about their APIs.


Workflow
Providers submit APIs, which are initially marked as "in review."
Administrators are notified via email for new API submissions.
Upon approval, the API status is updated to "live," and the data is copied to the API listings table.
Approved APIs appear on the home page for users to access.


Submission HTML Form
The submission form includes the following fields:
API Name
Short Description
Documentation URL
Long Description
Logo URL
Pricing Plans URL
Response Example








Database Structure for API Submissions and Listings
	
          




Submission Form
The submission form includes the following fields:
API Name
Short Description
Documentation URL
Long Description
Logo URL
Pricing Plans URL
Response Example




User Sign Up
Registration Process


The user sign-up process has been streamlined. Users are required to provide:
Full Name
Email
Password
Country




Password Toggle Feature
A new feature allows users to toggle password visibility on or off before submitting the form. 

A new block of code was added to support this feature.



 function togglePasswordVisibility() {
 	if (passwordInput.type === "password") {
 	passwordInput.type = "text"; // Show the password
 	slashed_eye_icon.style.display = 'block'
 	eye_icon.style.display = 'none'
 } else {
 	passwordInput.type = "password"; // Hide the password
 	slashed_eye_icon.style.display = 'none'
 	eye_icon.style.display = 'block'
 }
}










Navigation Bar


UI Modifications
The navigation bar has undergone UI updates per request. It now includes options for:

STYLING:
Updated the css styling accommodate the changes requested which includes the font-size, color and placeholder
 1. Login,
 2. sign up
 3. Documentation
 4. Adding APIs.

















Home Page


API Rendering
The home page displays both prompt api APIs and provider-created APIs. Users can click on provider-created APIs to view more details, including the product page.


Product Page
In the product page for provider-created APIs, Documentation and Pricing plans are accessible through links supplied during submission by the provider as opposed to viewable tabs on default apis product page.




















Login-Zero State Page
Different redirect scenarios on a user’s login event was implemented as listed below
User Redirect Scenarios :
Scenario 1: Users creating a profile for the first time are directed to the Portal homepage, where they can explore the marketplace or add their API (Zero State Page).
Scenario 2: Users with previous marketplace API subscriptions are redirected to the subscriptions section of the dashboard.
Scenario 3: Users with their own APIs onboarded to the marketplace are directed to the API list section in the dashboard.
Scenario 4: Users with marketplace API subscriptions and their own APIs onboarded are redirected to a customized dashboard section based on their preferences.


Product Page
The product page was initially generated using description_v2.html. However, a new description_v3.html file was introduced to display provider-created APIs. Both templates share a striking resemblance in terms of rendering content to end users, but they operate with distinct data objects. Presently, description_v2.html is employed for rendering the default API product page, while description_v3.html is utilized for provider-created APIs. A notable contrast in the user interface between the two templates is outlined below:

Fig 6.1: Default API on product page


Fig 6.1: Provider-created API on product page


When comparing Figure 6.1 to Figure 6.2, we observe that the pricing and documentation tabs in Figure 6.1 have been transformed into links in Figure 6.2. Figure 6.2 provides information about an API developed by a provider, and these links direct users to the web pages provided by the provider during API submission.



STYLESHEET

A custom.css file was added on project to house custom styles on elements used on the prompt-web which can me found in:

app/assets/css/custom.css






