// the specific URL for a given wordform (refactored from previous commits).
// TODO: should come from config.
const BASE_URL = 'https://sapir.artsrn.ualberta.ca/validation'

// the specific URL for a given speaker (appended with the speaker code)
const BASE_SPEAKER_URL = 'http://altlab.ualberta.ca/maskwacis/Speakers/';

export function fetchRecordings(wordform) {
  return fetch(`${BASE_URL}/recording/_search/${wordform}`)
    .then(function (response) {
      return response.json()
    })
}

export async function fetchFirstRecordingURL(wordform) {
  let results = await fetchRecordings(wordform)
  return results[0]['recording_url']
}


/**
 * Render a list of speakers (in button form) for the user to interact with and hear the wordform pronounced in different ways.
 */
export function retrieveListOfSpeakers() {
  // get the value of the wordform from the page
  let wordform = document.getElementById('data:head').value
  let derivedURL = `${BASE_URL}/recording/_search/${wordform}`

  let template = document.getElementById('template:recording-item')
  let recordingsList = document.querySelector('.recordings-list')

  // Request the JSON for all recordings of this wordform
  fetch(derivedURL)
    .then(request => request.json())
    .then(returnedData => {
      let numberOfRecordings = returnedData.length // number of records on the server

      // Unhide the explainer text
      let recordingsHeading = document.querySelector('.definition__recordings--not-loaded')
      recordingsHeading.classList.remove('definition__recordings--not-loaded')

      // we only want to display our list of speakers once!
      if (recordingsList.childElementCount < numberOfRecordings) {
        displaySpeakerList(returnedData)
      }
    })

  ////////////////////////////////// helpers /////////////////////////////////

  // the function that displays an individual speaker's name
  function displaySpeakerList(recordings) {
    for (let recordingData of recordings) {
      // Create the list element
      let individualSpeaker = template.content.firstChild.cloneNode(true)
      // put the list item into the DOM
      recordingsList.appendChild(individualSpeaker)
      setupButton(individualSpeaker, recordingData)
    }
  }

  function setupButton(createdSpeakerButton, recordingData) {
    // Add appropriate text
    createdSpeakerButton.querySelector('slot[name="speaker-name"]')
      .innerText = recordingData['speaker_name']
    // TODO: this should be derived from the recording JSON
    // TODO: as of 2020-06-04, it does not include this data :(
    createdSpeakerButton.querySelector('slot[name="speaker-dialect"]')
      .innerText = 'Maskwacîs'

    // Setup audio
    let audio = new Audio(recordingData.recording_url)
    audio.preload = 'none'
    createdSpeakerButton.addEventListener('click', () => {
      audio.play()
      displaySpeakerBioLink(recordingData);     
    })
  }

  // the function that creates a link for an individual speaker's bio to be clicked
  function displaySpeakerBioLink(recordingData) {
    let insertedURL = BASE_SPEAKER_URL + recordingData['speaker'] + '.html';

    // select for the area to place the speaker link
    let container = document.querySelector('.speaker-link');

    // select for the template
    let displaySpeakerTemplate = document.getElementById('template:speaker-bio-link').content.cloneNode(true);

    // create the speaker link URL
    let createdLink = displaySpeakerTemplate.firstChild;
    
    // variable to be inserted into the DOM
    let speakerName = recordingData['speaker_name'];

    // generate a new link and append it to the page if there isn't already one
    if (container.childElementCount < 1) {
      // set the speaker-link text with the name of the speaker
      displaySpeakerTemplate.querySelector('slot[name="speaker-name"]').innerText = speakerName;

      // set the link URL
      createdLink.href = insertedURL;

      // place the link into the template
      displaySpeakerTemplate.appendChild(createdLink);

      // place the template into the DOM
      container.appendChild(displaySpeakerTemplate);   
    } 
       
  }
}

// TODOkobe: Once everything is working, play with a way to dynamically indicate (on the button) that a repeat 'speaker' is a v1, v2, v3, etc
