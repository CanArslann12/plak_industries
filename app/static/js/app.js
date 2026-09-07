async function sendLead(form) {
  const response = await fetch('/api/leads', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(Object.fromEntries(new FormData(form)))
  });
  const result = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(result.hata || `Sunucu hatası (${response.status})`);
  return result;
}

document.querySelector('#lead-form')?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const status = document.querySelector('#form-status');
  const button = form.querySelector('button');
  button.disabled = true;
  status.textContent = 'Gönderiliyor...';
  try {
    const result = await sendLead(form);
    status.textContent = result.basari
      ? (result.bildirim_gonderildi ? 'Talebiniz kaydedildi ve PLAK INDUSTRIES ekibine iletildi.' : 'Talebiniz kaydedildi. E-posta bildirimi henüz yapılandırılmadı.')
      : (result.hata || 'Kayıt başarısız.');
    if (result.basari) form.reset();
  } catch (error) { status.textContent = error.message || 'Sunucuya ulaşılamadı.'; }
  button.disabled = false;
});

const chatHistory = [];

function addChatMessage(role, content) {
  const messages = document.querySelector('#chat-messages');
  if (!messages) return;
  messages.querySelector('.chat-empty')?.remove();
  const message = document.createElement('div');
  message.className = `chat-message chat-${role}`;
  message.dataset.role = role;
  message.textContent = content;
  messages.append(message);
  messages.scrollTop = messages.scrollHeight;
}

document.querySelector('#chat-clear')?.addEventListener('click', () => {
  chatHistory.length = 0;
  const messages = document.querySelector('#chat-messages');
  messages.innerHTML = '<p class="chat-empty">Sohbet temizlendi. Yeni sorunuzu yazabilirsiniz.</p>';
  document.querySelector('#chat-status').textContent = '';
});

document.querySelector('#chat-form')?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const status = document.querySelector('#chat-status');
  const button = event.currentTarget.querySelector('button');
  const messageInput = event.currentTarget.mesaj;
  const message = messageInput.value.trim();
  if (!message) return;
  button.disabled = true;
  status.textContent = 'Yanıt hazırlanıyor...';
  addChatMessage('user', message);
  messageInput.value = '';
  try {
    const response = await fetch('/api/sohbet', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ mesaj: message, gecmis: chatHistory }) });
    const result = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(result.hata || `Sunucu hatası (${response.status})`);
    if (!result.basari) throw new Error(result.hata || 'Yanıt alınamadı.');
    chatHistory.push({ role: 'user', content: message }, { role: 'assistant', content: result.cevap });
    addChatMessage('assistant', result.cevap);
    status.textContent = '';
  } catch (error) { status.textContent = error.message || 'Sunucuya ulaşılamadı.'; }
  button.disabled = false;
});

document.querySelector('#chat-message')?.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    event.currentTarget.form.requestSubmit();
  }
});

fetch('/api/ai-durum')
  .then((response) => response.json())
  .then((result) => {
    const status = document.querySelector('#ai-config-status');
    if (status) status.textContent = result.yapilandirilmis ? `SİSTEM AKTİF · ${result.saglayici.toUpperCase()}` : 'SİSTEM YAPILANDIRILMAMIŞ';
  })
  .catch(() => {
    const status = document.querySelector('#ai-config-status');
    if (status) status.textContent = 'API durumu alınamadı. Uygulamanın çalıştığını kontrol edin.';
  });
