const messageForm = document.getElementById('message-form');
const messageInput = document.getElementById('message-input');

messageForm.addEventListener('submit', (e) => {
  e.preventDefault();
  
  const recipientId = messageForm.dataset.recipientId;
  const messageContent = messageInput.value;

  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/send_message');
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onload = () => {
    if (xhr.status === 200) {
      refreshMessages(recipientId);
      messageInput.value = ''; // Очистка поля ввода
    } else {
      console.error('Ошибка при отправке сообщения');
    }
  };
  xhr.send(JSON.stringify({ recipient_id: recipientId, message_content: messageContent }));
});

function refreshMessages(recipientId) {
  const xhr = new XMLHttpRequest();
  xhr.open('GET', `/chat/${recipientId}`);
  xhr.onload = () => {
    if (xhr.status === 200) {
      const messageContainer = document.getElementById('message-container');
      messageContainer.innerHTML = xhr.responseText;
    } else {
      console.error('Ошибка при получении списка сообщений');
    }
  };
  xhr.send();
}

const recipientId = messageForm.dataset.recipientId;
refreshMessages(recipientId);
