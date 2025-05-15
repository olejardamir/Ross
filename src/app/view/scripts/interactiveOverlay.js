const clickableAreaA = document.getElementById('clickableAreaA');
const textField = document.getElementById('textField');
const textArea = document.getElementById('textArea');
const overlay = document.querySelector('.overlay');
const spinner = document.getElementById('spinner');

clickableAreaA.addEventListener('click', async () => {
  const topic = textField.value.trim();

  if (topic.length < 10) {
    alert('Text is too short');
    return;
  }

  // Show spinner and disable interface
  spinner.style.display = 'flex';
  overlay.classList.add('disabled');

  try {
    const response = await fetch('https://localhost:8000/speech', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ topic }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const responseData = await response.json();

    // Place response text in the textarea
    textArea.value = responseData.speech || 'No text field in response.';

  } catch (error) {
    alert('Failed to generate speech: ' + error.message);
  } finally {
    // Hide spinner and re-enable interface
    spinner.style.display = 'none';
    overlay.classList.remove('disabled');
  }
});


//========================== AREA B
const clickableAreaB = document.getElementById('clickableAreaB');

clickableAreaB.addEventListener('click', async () => {
  const topic = textField.value.trim();
  const speech = textArea.value.trim();

  if (topic.length < 10 || speech.length < 100) {
    alert('Please enter a topic and a sufficiently long speech.');
    return;
  }

  // Show spinner and disable interface
  spinner.style.display = 'flex';
  overlay.classList.add('disabled');

  try {
    const response = await fetch('https://localhost:8000/text2video', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ topic, speech }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const responseData = await response.json();

    if (responseData.message === "done") {
      showVideoModal('app/utils/core/tmp/final_output.mp4');
    } else {
      alert('Unexpected response from server.');
    }

  } catch (error) {
    alert('Failed to generate video: ' + error.message);
  } finally {
    spinner.style.display = 'none';
    overlay.classList.remove('disabled');
  }
});

// Function to show the modal with video
function showVideoModal(videoPath) {
  const modalOverlay = document.createElement('div');
  modalOverlay.classList.add('modal-overlay');

  const modalContent = document.createElement('div');
  modalContent.classList.add('modal-content');

  const video = document.createElement('video');
  video.src = videoPath;
  video.controls = true;
  video.autoplay = true;
  video.style.maxWidth = '90%';
  video.style.maxHeight = '90%';

  modalContent.appendChild(video);
  modalOverlay.appendChild(modalContent);
  document.body.appendChild(modalOverlay);

  // Close modal when clicking outside the video
  modalOverlay.addEventListener('click', (event) => {
    if (event.target === modalOverlay) {
      document.body.removeChild(modalOverlay);
    }
  });
}

