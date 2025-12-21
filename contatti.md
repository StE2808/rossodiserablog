---
layout: default
title: Contatti
permalink: /contatti/
---

<section class="contact-section">
    <header class="section-header">
        <span class="section-label">Scrivici</span>
        <h1 class="section-title">Contatti</h1>
        <p class="section-description">Hai una domanda, un suggerimento o vuoi semplicemente dirci la tua? Compila il form qui sotto e ti risponderemo al più presto.</p>
    </header>

    <div class="contact-container">
        <form id="contact-form" class="contact-form">
            <div class="form-group">
                <label for="nome">Nome *</label>
                <input type="text" id="nome" name="nome" required placeholder="Il tuo nome">
            </div>
            
            <div class="form-group">
                <label for="email">Email *</label>
                <input type="email" id="email" name="email" required placeholder="La tua email">
            </div>
            
            <div class="form-group">
                <label for="messaggio">Messaggio *</label>
                <textarea id="messaggio" name="messaggio" rows="6" required placeholder="Scrivi qui il tuo messaggio..."></textarea>
            </div>
            
            <button type="submit" class="submit-btn" id="submit-btn">
                <span class="btn-text">Invia messaggio</span>
                <span class="btn-loading" style="display: none;">Invio in corso...</span>
                <svg class="btn-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
                </svg>
            </button>
        </form>
        
        <div id="form-success" class="form-message success" style="display: none;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
            <p>Grazie per il tuo messaggio! Ti risponderemo al più presto.</p>
        </div>
        
        <div id="form-error" class="form-message error" style="display: none;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="15" y1="9" x2="9" y2="15"/>
                <line x1="9" y1="9" x2="15" y2="15"/>
            </svg>
            <p>Si è verificato un errore. Riprova più tardi o scrivici direttamente via email.</p>
        </div>
    </div>
</section>

<script>
document.getElementById('contact-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const form = this;
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoading = submitBtn.querySelector('.btn-loading');
    const successMsg = document.getElementById('form-success');
    const errorMsg = document.getElementById('form-error');
    
    // Disabilita il pulsante e mostra loading
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline';
    
    // Nascondi messaggi precedenti
    successMsg.style.display = 'none';
    errorMsg.style.display = 'none';
    
    const data = {
        nome: document.getElementById('nome').value,
        email: document.getElementById('email').value,
        messaggio: document.getElementById('messaggio').value
    };
    
    try {
        const response = await fetch('https://script.google.com/macros/s/AKfycbw6iMfn_2EuG22aBKgUPvZLPpmYQ1yf8p8y5ThzzzBFF-CQW1EYGUcdN8On7z9TV-ERwg/exec', {
            method: 'POST',
            mode: 'no-cors',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        // Con no-cors non possiamo leggere la risposta, assumiamo successo
        form.style.display = 'none';
        successMsg.style.display = 'flex';
        form.reset();
        
    } catch (error) {
        errorMsg.style.display = 'flex';
        console.error('Errore:', error);
    } finally {
        // Riabilita il pulsante
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    }
});
</script>
