/* ==========================================================================
   Krishi Sahayak — Chat Application with Image Support
   ========================================================================== */

(function($) {
    'use strict';

    var WELCOME = '<div class="welcome">'
        + '<div class="welcome-icon"><i class="bi bi-flower2"></i></div>'
        + '<h3>Krishi Sahayak</h3>'
        + '<p>Your AI agriculture assistant. Ask anything about crops, pests, soil, or share a photo for diagnosis.</p>'
        + '<div class="chips">'
        + '<span class="chip" data-text="What is the best time to plant wheat in India?"><i class="bi bi-calendar3"></i> Wheat planting season</span>'
        + '<span class="chip" data-text="How to control pest attack on tomato plants?"><i class="bi bi-bug"></i> Tomato pest control</span>'
        + '<span class="chip" data-text="What fertilizer is good for paddy rice?"><i class="bi bi-droplet"></i> Paddy fertilizer</span>'
        + '<span class="chip" data-text="Tell me about PM-KISAN scheme eligibility"><i class="bi bi-card-list"></i> PM-KISAN scheme</span>'
        + '</div></div>';

    var mediaRecorder = null, audioChunks = [], isRecording = false, isProcessing = false;
    var selectedImage = null;

    var $messages = $('#chatMessages'), $form = $('#chatForm'), $input = $('#userInput');
    var $sendBtn = $('#sendBtn'), $voiceBtn = $('#voiceBtn'), $typing = $('#typingIndicator');
    var $audio = $('#audioPlayer'), $clearBtn = $('#clearBtn'), $themeBtn = $('#themeToggle');
    var $themeIcon = $('#themeIcon'), $imageBtn = $('#imageBtn'), $imageInput = $('#imageInput');
    var $preview = $('#imagePreview'), $previewImg = $('#previewImg'), $removeImg = $('#removeImage');

    // ── Init ──
    $(document).ready(function() {
        initTheme(); showWelcome(); updateDate();
        $form.on('submit', handleSend);
        $input.on('keydown', function(e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); $form.trigger('submit'); } });
        $voiceBtn.on('click', toggleRecording);
        $clearBtn.on('click', clearConversation);
        $themeBtn.on('click', toggleTheme);
        $imageBtn.on('click', function() { $imageInput.trigger('click'); });
        $imageInput.on('change', handleImageSelect);
        $removeImg.on('click', clearImage);
        $messages.on('click', '.chip', function() { var t = $(this).data('text'); if (t) { $input.val(t); $form.trigger('submit'); } });
        if ('Notification' in window && Notification.permission === 'default') Notification.requestPermission();
        $input.trigger('focus');
    });

    // ── Theme ──
    function initTheme() {
        if (localStorage.getItem('agri-bot-theme') === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
            $themeIcon.removeClass('bi-moon-stars-fill').addClass('bi-sun-fill');
        }
    }
    function toggleTheme() {
        var dark = document.documentElement.getAttribute('data-theme') === 'dark';
        document.documentElement[dark ? 'removeAttribute' : 'setAttribute']('data-theme', 'dark');
        localStorage.setItem('agri-bot-theme', dark ? 'light' : 'dark');
        $themeIcon.toggleClass('bi-moon-stars-fill bi-sun-fill');
    }

    // ── Helpers ──
    function showWelcome() { $messages.html(WELCOME); }
    function updateDate() { $('#dateDisplay').text(new Date().toLocaleDateString('en-IN', { weekday: 'short', month: 'short', day: 'numeric' })); }
    function scrollBottom() { $messages.stop().animate({ scrollTop: $messages[0].scrollHeight }, 250); }
    function getTime() { return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }); }
    function showTyping() { $typing.addClass('visible'); scrollBottom(); }
    function hideTyping() { $typing.removeClass('visible'); }
    function esc(t) { var d = document.createElement('div'); d.textContent = t; return d.innerHTML; }

    // ── Image Handling ──
    function handleImageSelect(e) {
        var file = e.target.files[0];
        if (!file) return;
        if (file.size > 4 * 1024 * 1024) { showToast('Image too large. Max 4MB allowed.'); return; }
        if (!file.type.startsWith('image/')) { showToast('Please select an image file.'); return; }
        selectedImage = file;
        var reader = new FileReader();
        reader.onload = function(ev) {
            $previewImg.attr('src', ev.target.result);
            $preview.addClass('active');
        };
        reader.readAsDataURL(file);
        $imageBtn.addClass('active');
    }

    function clearImage() {
        selectedImage = null;
        $imageInput.val('');
        $preview.removeClass('active');
        $previewImg.attr('src', '');
        $imageBtn.removeClass('active');
    }

    // ── Messages ──
    function addMessage(text, type, cache, imageUrl) {
        var isUser = type === 'user';
        var icon = isUser ? 'bi-person-fill' : 'bi-flower2';
        var imgTag = imageUrl ? '<img class="msg-img" src="' + imageUrl + '" alt="Shared image">' : '';

        if (isUser && $messages.find('.welcome').length) $messages.find('.welcome').remove();

        var cacheTag = '';
        if (cache && cache.cached_tokens > 0) {
            cacheTag = '<span class="cache-tag"><i class="bi bi-lightning-fill"></i>' + cache.hit_rate + '% cached</span>';
        }

        var html = '<div class="msg ' + type + '">'
            + '<div class="msg-av"><i class="bi ' + icon + '"></i></div>'
            + '<div class="bubble">'
            + imgTag
            + '<div>' + esc(text).replace(/\n/g, '<br>') + '</div>'
            + '<div class="msg-meta"><span>' + getTime() + '</span>' + cacheTag + '</div>'
            + '</div></div>';

        $messages.append(html);
        scrollBottom();
    }

    // ── Send Text or Image ──
    function handleSend(e) {
        e.preventDefault();
        var text = $input.val().trim();
        var hasImage = selectedImage !== null;

        if (!text && !hasImage) return;
        if (isProcessing) return;
        if (!text && hasImage) text = 'What do you see in this image? Please analyze from an agricultural perspective.';

        isProcessing = true;
        $input.val('');
        $sendBtn.prop('disabled', true);
        $voiceBtn.prop('disabled', true);
        $imageBtn.prop('disabled', true);

        // Save reference before clearing preview
        var imageToSend = selectedImage;
        var imgPreviewUrl = imageToSend ? $previewImg.attr('src') : null;
        addMessage(text, 'user', null, imgPreviewUrl);
        clearImage();
        showTyping();

        if (hasImage) {
            // Upload as multipart form
            var fd = new FormData();
            fd.append('image', imageToSend, imageToSend.name || 'image.jpg');
            fd.append('text', text);

            $.ajax({ url: '/chat', type: 'POST', data: fd, contentType: false, processData: false, timeout: 60000 })
            .done(function(r) { hideTyping(); if (r.text) { addMessage(r.text, 'bot', r.cache); playVoice(r.voice); } })
            .fail(function(x) { hideTyping(); addMessage(getError(x), 'bot'); })
            .always(done);
        } else {
            $.ajax({ url: '/chat', type: 'POST', data: { text: text }, timeout: 60000 })
            .done(function(r) { hideTyping(); if (r.text) { addMessage(r.text, 'bot', r.cache); playVoice(r.voice); } })
            .fail(function(x) { hideTyping(); addMessage(getError(x), 'bot'); })
            .always(done);
        }

        function done() {
            isProcessing = false;
            $sendBtn.prop('disabled', false);
            $voiceBtn.prop('disabled', false);
            $imageBtn.prop('disabled', false);
            $input.trigger('focus');
        }
    }

    function playVoice(src) {
        if (!src) return;
        $audio.attr('src', src);
        $audio[0].play().catch(function() {});
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification('Krishi Sahayak', { body: 'Voice response ready', icon: '/static/images/favicon.ico' });
        }
    }

    function getError(xhr) {
        if (xhr.status === 400 && xhr.responseJSON) return xhr.responseJSON.error || 'Bad request.';
        if (xhr.status === 429) return 'Too many requests. Please wait.';
        if (xhr.statusText === 'timeout') return 'Request timed out. Try again.';
        return 'Something went wrong. Please try again.';
    }

    // ── Voice Recording ──
    function toggleRecording() { isRecording ? stopRecording() : startRecording(); }

    async function startRecording() {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) { showToast('Voice not supported.'); return; }
        try {
            var stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            audioChunks = [];
            mediaRecorder = new MediaRecorder(stream, { mimeType: MediaRecorder.isTypeSupported('audio/webm;codecs=opus') ? 'audio/webm;codecs=opus' : 'audio/webm' });
            mediaRecorder.ondataavailable = function(e) { if (e.data.size > 0) audioChunks.push(e.data); };
            mediaRecorder.onstop = function() { sendAudio(new Blob(audioChunks, { type: 'audio/webm' })); stream.getTracks().forEach(function(t) { t.stop(); }); };
            mediaRecorder.onerror = function() { showToast('Mic error.'); stream.getTracks().forEach(function(t) { t.stop(); }); isRecording = false; $voiceBtn.removeClass('recording'); };
            mediaRecorder.start(250);
            isRecording = true;
            $voiceBtn.addClass('recording');
            showToast('Recording...');
        } catch (err) { showToast('Mic access denied.'); }
    }

    function stopRecording() { if (mediaRecorder && mediaRecorder.state !== 'inactive') mediaRecorder.stop(); isRecording = false; $voiceBtn.removeClass('recording'); }

    function sendAudio(blob) {
        if (isProcessing) return;
        isProcessing = true; $sendBtn.prop('disabled', true); $voiceBtn.prop('disabled', true); showTyping();
        var fd = new FormData(); fd.append('audio', blob, 'recording.webm');
        $.ajax({ url: '/chat', type: 'POST', data: fd, contentType: false, processData: false, timeout: 30000 })
        .done(function(r) { hideTyping(); if (r.transcription) addMessage(r.transcription, 'user'); if (r.text) { addMessage(r.text, 'bot', r.cache); playVoice(r.voice); } })
        .fail(function(x) { hideTyping(); addMessage('Could not process audio.', 'bot'); })
        .always(function() { isProcessing = false; $sendBtn.prop('disabled', false); $voiceBtn.prop('disabled', false); $input.trigger('focus'); });
    }

    // ── Clear ──
    function clearConversation() {
        if (!$messages.find('.msg').length) return;
        if (!confirm('Clear this conversation?')) return;
        $.post('/chat/clear', function() { showWelcome(); $audio.attr('src', ''); $input.trigger('focus'); });
    }

    // ── Toast ──
    function showToast(msg) {
        $('.toast-msg').remove();
        var t = $('<div class="toast-msg"><i class="bi bi-info-circle me-1" style="color:var(--primary)"></i>' + esc(msg) + '</div>');
        $('body').append(t); t.fadeIn(200);
        setTimeout(function() { t.fadeOut(200, function() { $(this).remove(); }); }, 3000);
    }

})(jQuery);