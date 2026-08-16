// ============================================================
// 🤖 MALiYA AI - FULL SCRIPT
// ============================================================


// ============================================================
// BASIC ELEMENTS
// ============================================================

const input =
    document.getElementById(
        "messageInput"
    );

const sendButton =
    document.getElementById(
        "sendButton"
    );

const micButton =
    document.getElementById(
        "micButton"
    );

const chat =
    document.getElementById(
        "chat"
    );


// ============================================================
// SETTINGS
// ============================================================

const settingsButton =
    document.getElementById(
        "settingsButton"
    );

const settingsPanel =
    document.getElementById(
        "settingsPanel"
    );

const closeSettings =
    document.getElementById(
        "closeSettings"
    );

const voiceOutput =
    document.getElementById(
        "voiceOutput"
    );

const voiceInput =
    document.getElementById(
        "voiceInput"
    );

const voiceSpeed =
    document.getElementById(
        "voiceSpeed"
    );


// ============================================================
// MEMORY
// ============================================================

const memoryButton =
    document.getElementById(
        "memoryButton"
    );

const memoryPanel =
    document.getElementById(
        "memoryPanel"
    );

const closeMemory =
    document.getElementById(
        "closeMemory"
    );

const memoryList =
    document.getElementById(
        "memoryList"
    );

const clearMemory =
    document.getElementById(
        "clearMemory"
    );


// ============================================================
// ACCOUNT
// ============================================================

const accountButton =
    document.getElementById(
        "accountButton"
    );

const accountMenu =
    document.getElementById(
        "accountMenu"
    );

const logoutButton =
    document.getElementById(
        "logoutButton"
    );

const accountPhoto =
    document.getElementById(
        "accountPhoto"
    );

const accountName =
    document.getElementById(
        "accountName"
    );

const menuPhoto =
    document.getElementById(
        "menuPhoto"
    );

const menuName =
    document.getElementById(
        "menuName"
    );

const menuEmail =
    document.getElementById(
        "menuEmail"
    );


// ============================================================
// AUTH
// ============================================================

let currentUser =
    null;


// ============================================================
// AUTH USER SETUP
// ============================================================

function setupUser(user) {

    if (!user) {

        console.log(
            "❌ No Firebase user"
        );

        return;

    }


    currentUser =
        user;


    window.maliyaUser =
        user;


    console.log(
        "✅ User ready:",
        user.email
    );


    // ========================================================
    // USER DETAILS
    // ========================================================

    const name =
        user.displayName ||
        "Maliya User";


    const email =
        user.email ||
        "";


    const photo =
        user.photoURL ||
        "";


    // ========================================================
    // ACCOUNT BUTTON
    // ========================================================

    if (accountName) {

        accountName.textContent =
            name;

    }


    if (accountPhoto) {

        if (photo) {

            accountPhoto.src =
                photo;

            accountPhoto.style.display =
                "block";

        }

        else {

            accountPhoto.style.display =
                "none";

        }

    }


    // ========================================================
    // ACCOUNT MENU
    // ========================================================

    if (menuName) {

        menuName.textContent =
            name;

    }


    if (menuEmail) {

        menuEmail.textContent =
            email;

    }


    if (menuPhoto) {

        if (photo) {

            menuPhoto.src =
                photo;

            menuPhoto.style.display =
                "block";

        }

        else {

            menuPhoto.style.display =
                "none";

        }

    }


    // ========================================================
    // ENABLE CHAT
    // ========================================================

    if (input) {

        input.disabled =
            false;

    }


    if (sendButton) {

        sendButton.disabled =
            false;

    }


    if (micButton) {

        micButton.disabled =
            false;

    }


    if (input) {

        input.focus();

    }

}


// ============================================================
// AUTH READY EVENT
// ============================================================

document.addEventListener(
    "maliya-auth-ready",
    function (event) {

        setupUser(
            event.detail
        );

    }
);


// ============================================================
// IMPORTANT:
// Firebase module may finish BEFORE script.js loads.
// So check window.maliyaUser too.
// ============================================================

if (window.maliyaUser) {

    setupUser(
        window.maliyaUser
    );

}


// ============================================================
// GET AUTH HEADERS
// ============================================================

async function getAuthHeaders() {

    const auth =
        window.maliyaAuth;


    if (!auth) {

        throw new Error(
            "Firebase Auth not initialized"
        );

    }


    const user =
        auth.currentUser;


    if (!user) {

        throw new Error(
            "Authentication required"
        );

    }


    currentUser =
        user;


    /*
       Force refresh the Firebase ID token.
       This helps when an old token expires.
    */

    const token =
        await user.getIdToken(
            true
        );


    return {

        "Content-Type":
            "application/json",

        "Authorization":
            "Bearer " + token

    };

}


// ============================================================
// ADD MESSAGE
// ============================================================

function addMessage(
    text,
    type
) {

    if (!chat) {

        return;

    }


    const message =
        document.createElement(
            "div"
        );


    message.className =
        "message " +
        type +
        "-message";


    const avatar =
        document.createElement(
            "div"
        );


    avatar.className =
        "avatar";


    avatar.textContent =
        type === "user"
            ? "👤"
            : "🤖";


    const bubble =
        document.createElement(
            "div"
        );


    bubble.className =
        "bubble";


    bubble.textContent =
        text;


    message.appendChild(
        avatar
    );


    message.appendChild(
        bubble
    );


    chat.appendChild(
        message
    );


    chat.scrollTop =
        chat.scrollHeight;

}


// ============================================================
// 🔊 VOICE OUTPUT
// ============================================================

function speakText(text) {

    if (
        !voiceOutput ||
        !voiceOutput.checked
    ) {

        return;

    }


    if (
        !(
            "speechSynthesis"
            in window
        )
    ) {

        console.log(
            "❌ Browser voice output unavailable"
        );

        return;

    }


    window.speechSynthesis.cancel();


    const speech =
        new SpeechSynthesisUtterance(
            text
        );


    // ========================================================
    // LANGUAGE
    // ========================================================

    speech.lang =
        "si-LK";


    // ========================================================
    // SPEED
    // ========================================================

    speech.rate =
        parseFloat(
            voiceSpeed?.value ||
            "1"
        );


    speech.pitch =
        1;


    speech.volume =
        1;


    // ========================================================
    // FIND SINHALA VOICE
    // ========================================================

    const voices =
        window.speechSynthesis
            .getVoices();


    let selectedVoice =
        voices.find(
            function (voice) {

                return voice.lang
                    .toLowerCase()
                    .startsWith("si");

            }
        );


    // ========================================================
    // ENGLISH FALLBACK
    // ========================================================

    if (!selectedVoice) {

        selectedVoice =
            voices.find(
                function (voice) {

                    return voice.lang
                        .toLowerCase()
                        .startsWith("en");

                }
            );

    }


    if (selectedVoice) {

        speech.voice =
            selectedVoice;

        console.log(
            "🔊 Voice:",
            selectedVoice.name,
            selectedVoice.lang
        );

    }


    window.speechSynthesis.speak(
        speech
    );

}


// ============================================================
// STOP VOICE
// ============================================================

function stopVoice() {

    if (
        "speechSynthesis"
        in window
    ) {

        window.speechSynthesis.cancel();

    }

}


// ============================================================
// 💬 SEND MESSAGE
// ============================================================

async function sendMessage() {

    const text =
        input
            ? input.value.trim()
            : "";


    if (!text) {

        return;

    }


    if (!currentUser) {

        addMessage(
            "❌ Authentication required",
            "ai"
        );

        return;

    }


    // ========================================================
    // SHOW USER MESSAGE
    // ========================================================

    addMessage(
        text,
        "user"
    );


    input.value =
        "";


    sendButton.disabled =
        true;


    try {

        // ====================================================
        // AUTH
        // ====================================================

        const headers =
            await getAuthHeaders();


        // ====================================================
        // API
        // ====================================================

        const response =
            await fetch(
                "/api/chat",
                {

                    method:
                        "POST",

                    headers:
                        headers,

                    body:
                        JSON.stringify({

                            message:
                                text

                        })

                }
            );


        const data =
            await response.json();


        // ====================================================
        // AUTH ERROR
        // ====================================================

        if (
            response.status ===
            401
        ) {

            addMessage(
                "❌ Login session එක expire වෙලා. නැවත login වෙන්න.",
                "ai"
            );

            return;

        }


        // ====================================================
        // SUCCESS
        // ====================================================

        if (data.success) {

            addMessage(
                data.answer,
                "ai"
            );


            // ==================================================
            // VOICE
            // ==================================================

            speakText(
                data.answer
            );

        }


        // ====================================================
        // API ERROR
        // ====================================================

        else {

            addMessage(

                "❌ " +
                (
                    data.error ||
                    "Unknown error"
                ),

                "ai"

            );

        }

    }

    catch (error) {

        console.error(
            "❌ Chat error:",
            error
        );


        addMessage(

            "❌ " +
            error.message,

            "ai"

        );

    }


    sendButton.disabled =
        false;


    if (input) {

        input.focus();

    }

}


// ============================================================
// SEND BUTTON
// ============================================================

if (sendButton) {

    sendButton.addEventListener(
        "click",
        sendMessage
    );

}


// ============================================================
// ENTER KEY
// ============================================================

if (input) {

    input.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key ===
                "Enter"
            ) {

                event.preventDefault();

                sendMessage();

            }

        }
    );

}


// ============================================================
// 🎤 VOICE INPUT
// ============================================================

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;


let recognition =
    null;


let listening =
    false;


if (
    SpeechRecognition &&
    micButton
) {

    recognition =
        new SpeechRecognition();


    recognition.lang =
        "si-LK";


    recognition.continuous =
        false;


    recognition.interimResults =
        false;


    recognition.maxAlternatives =
        1;


    // ========================================================
    // MIC BUTTON
    // ========================================================

    micButton.addEventListener(
        "click",
        function () {

            if (
                voiceInput &&
                !voiceInput.checked
            ) {

                return;

            }


            if (!currentUser) {

                return;

            }


            if (listening) {

                recognition.stop();

                return;

            }


            try {

                recognition.start();

            }

            catch (error) {

                console.log(
                    "🎤 Mic error:",
                    error
                );

            }

        }
    );


    // ========================================================
    // START
    // ========================================================

    recognition.onstart =
        function () {

            listening =
                true;


            micButton.textContent =
                "🔴";


            micButton.classList.add(
                "recording"
            );

        };


    // ========================================================
    // RESULT
    // ========================================================

    recognition.onresult =
        function (event) {

            const text =
                event
                    .results[0][0]
                    .transcript;


            if (input) {

                input.value =
                    text;

            }


            sendMessage();

        };


    // ========================================================
    // END
    // ========================================================

    recognition.onend =
        function () {

            listening =
                false;


            micButton.textContent =
                "🎤";


            micButton.classList.remove(
                "recording"
            );

        };


    // ========================================================
    // ERROR
    // ========================================================

    recognition.onerror =
        function (event) {

            console.log(
                "🎤 Voice error:",
                event.error
            );


            listening =
                false;


            micButton.textContent =
                "🎤";


            micButton.classList.remove(
                "recording"
            );

        };

}

else {

    console.log(
        "⚠️ Speech Recognition not supported"
    );

}


// ============================================================
// 🧠 MEMORY - OPEN
// ============================================================

if (memoryButton) {

    memoryButton.addEventListener(
        "click",
        loadMemory
    );

}


// ============================================================
// MEMORY - CLOSE
// ============================================================

if (closeMemory) {

    closeMemory.addEventListener(
        "click",
        function () {

            if (memoryPanel) {

                memoryPanel.classList.remove(
                    "active"
                );

            }

        }
    );

}


// ============================================================
// LOAD MEMORY
// ============================================================

async function loadMemory() {

    if (!memoryPanel) {

        return;

    }


    memoryPanel.classList.add(
        "active"
    );


    if (memoryList) {

        memoryList.innerHTML = `

            <p class="empty-memory">
                🧠 Loading...
            </p>

        `;

    }


    try {

        const headers =
            await getAuthHeaders();


        const response =
            await fetch(
                "/api/memory",
                {

                    method:
                        "GET",

                    headers:
                        headers

                }
            );


        const data =
            await response.json();


        if (!data.success) {

            memoryList.innerHTML = `

                <p class="empty-memory">

                    ❌
                    ${escapeHTML(
                        data.error ||
                        "Memory load failed"
                    )}

                </p>

            `;

            return;

        }


        const memories =
            data.memory;


        if (
            !memories ||
            memories.length === 0
        ) {

            memoryList.innerHTML = `

                <p class="empty-memory">

                    🧠 Memory එකේ
                    conversation එකක් නැහැ.

                </p>

            `;

            return;

        }


        memoryList.innerHTML =
            "";


        memories
            .slice()
            .reverse()
            .forEach(
                function (item) {

                    const div =
                        document.createElement(
                            "div"
                        );


                    div.className =
                        "memory-item";


                    div.innerHTML = `

                        <div class="memory-time">

                            ${escapeHTML(
                                item.time || ""
                            )}

                        </div>


                        <div class="memory-user">

                            👤
                            <b>You:</b>

                            <br>

                            ${escapeHTML(
                                item.user || ""
                            )}

                        </div>


                        <div class="memory-ai">

                            🤖
                            <b>Maliya AI:</b>

                            <br>

                            ${escapeHTML(
                                item.assistant || ""
                            )}

                        </div>

                    `;


                    memoryList.appendChild(
                        div
                    );

                }
            );

    }

    catch (error) {

        console.error(
            "❌ Memory error:",
            error
        );


        if (memoryList) {

            memoryList.innerHTML = `

                <p class="empty-memory">

                    ❌
                    ${escapeHTML(
                        error.message
                    )}

                </p>

            `;

        }

    }

}


// ============================================================
// 🗑️ CLEAR MEMORY
// ============================================================

if (clearMemory) {

    clearMemory.addEventListener(
        "click",
        async function () {

            const confirmed =
                confirm(
                    "🗑️ මේ account එකේ memory එක clear කරන්නද?"
                );


            if (!confirmed) {

                return;

            }


            try {

                const headers =
                    await getAuthHeaders();


                const response =
                    await fetch(
                        "/api/memory/clear",
                        {

                            method:
                                "POST",

                            headers:
                                headers

                        }
                    );


                const data =
                    await response.json();


                if (data.success) {

                    memoryList.innerHTML = `

                        <p class="empty-memory">

                            🧹 Memory cleared.

                        </p>

                    `;

                }

                else {

                    alert(
                        "❌ " +
                        (
                            data.error ||
                            "Clear failed"
                        )
                    );

                }

            }

            catch (error) {

                console.error(
                    "❌ Clear memory:",
                    error
                );


                alert(
                    "❌ " +
                    error.message
                );

            }

        }
    );

}


// ============================================================
// ⚙️ SETTINGS - OPEN
// ============================================================

if (settingsButton) {

    settingsButton.addEventListener(
        "click",
        function () {

            if (settingsPanel) {

                settingsPanel.classList.add(
                    "active"
                );

            }

        }
    );

}


// ============================================================
// SETTINGS - CLOSE
// ============================================================

if (closeSettings) {

    closeSettings.addEventListener(
        "click",
        function () {

            if (settingsPanel) {

                settingsPanel.classList.remove(
                    "active"
                );

            }

        }
    );

}


// ============================================================
// LOAD SETTINGS
// ============================================================

function loadSettings() {

    const savedVoiceOutput =
        localStorage.getItem(
            "maliya_voice_output"
        );


    const savedVoiceInput =
        localStorage.getItem(
            "maliya_voice_input"
        );


    const savedVoiceSpeed =
        localStorage.getItem(
            "maliya_voice_speed"
        );


    if (voiceOutput) {

        voiceOutput.checked =
            savedVoiceOutput === "true";

    }


    if (voiceInput) {

        if (
            savedVoiceInput ===
            null
        ) {

            voiceInput.checked =
                true;

        }

        else {

            voiceInput.checked =
                savedVoiceInput ===
                "true";

        }

    }


    if (voiceSpeed) {

        voiceSpeed.value =
            savedVoiceSpeed ||
            "1";

    }

}


// ============================================================
// VOICE OUTPUT SETTING
// ============================================================

if (voiceOutput) {

    voiceOutput.addEventListener(
        "change",
        function () {

            localStorage.setItem(
                "maliya_voice_output",
                voiceOutput.checked
            );


            if (
                !voiceOutput.checked
            ) {

                stopVoice();

            }

        }
    );

}


// ============================================================
// VOICE INPUT SETTING
// ============================================================

if (voiceInput) {

    voiceInput.addEventListener(
        "change",
        function () {

            localStorage.setItem(
                "maliya_voice_input",
                voiceInput.checked
            );


            if (
                !voiceInput.checked &&
                listening &&
                recognition
            ) {

                recognition.stop();

            }

        }
    );

}


// ============================================================
// VOICE SPEED
// ============================================================

if (voiceSpeed) {

    voiceSpeed.addEventListener(
        "input",
        function () {

            localStorage.setItem(
                "maliya_voice_speed",
                voiceSpeed.value
            );

        }
    );

}


// ============================================================
// 👤 ACCOUNT BUTTON
// ============================================================

if (accountButton) {

    accountButton.addEventListener(
        "click",
        function (event) {

            event.stopPropagation();


            if (accountMenu) {

                accountMenu.classList.toggle(
                    "active"
                );

            }

        }
    );

}


// ============================================================
// CLOSE ACCOUNT MENU OUTSIDE
// ============================================================

document.addEventListener(
    "click",
    function (event) {

        if (
            accountMenu &&
            accountButton &&
            !accountMenu.contains(
                event.target
            ) &&
            !accountButton.contains(
                event.target
            )
        ) {

            accountMenu.classList.remove(
                "active"
            );

        }

    }
);


// ============================================================
// 🚪 LOGOUT
// ============================================================

if (logoutButton) {

    logoutButton.addEventListener(
        "click",
        async function () {

            const confirmed =
                confirm(
                    "🚪 Logout වෙන්නද?"
                );


            if (!confirmed) {

                return;

            }


            logoutButton.disabled =
                true;


            logoutButton.innerHTML =
                "⏳ Logging out...";


            try {

                if (
                    window.maliyaLogout
                ) {

                    await window.maliyaLogout();

                }

                else {

                    throw new Error(
                        "Logout function unavailable"
                    );

                }

            }

            catch (error) {

                console.error(
                    "❌ Logout error:",
                    error
                );


                logoutButton.disabled =
                    false;


                logoutButton.innerHTML =
                    "🚪 Logout";


                alert(
                    "❌ Logout failed: " +
                    error.message
                );

            }

        }
    );

}


// ============================================================
// 🔊 BROWSER VOICES
// ============================================================

if (
    "speechSynthesis"
    in window
) {

    window.speechSynthesis
        .addEventListener(
            "voiceschanged",
            function () {

                const voices =
                    window.speechSynthesis
                        .getVoices();


                console.log(
                    "🔊 Available voices:",
                    voices
                );

            }
        );

}


// ============================================================
// SECURITY
// ============================================================

function escapeHTML(text) {

    const div =
        document.createElement(
            "div"
        );


    div.textContent =
        text;


    return div.innerHTML;

}


// ============================================================
// START
// ============================================================

loadSettings();


console.log(
    "🤖 Maliya AI script loaded"
);

console.log(
    "🔐 Firebase authentication ready"
);

console.log(
    "🧠 User memory ready"
);

console.log(
    "🎤 Voice input ready"
);

console.log(
    "🔊 Voice output ready"
);