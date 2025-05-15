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

// Add click event for clickable area B
document.getElementById('clickableAreaB').addEventListener('click', () => {
  alert('Clickable area B was clicked!');
});
