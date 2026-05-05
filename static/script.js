let selectedUniverse = "";
const userId = localStorage.getItem('sorting_user_id') || 'user_' + Math.random().toString(36).substr(2, 9);
localStorage.setItem('sorting_user_id', userId);

function selectUniverse(universe) {
    selectedUniverse = universe;
    document.getElementById("selection-screen").style.display = "none";
    document.getElementById("sorting-ui").style.display = "flex";

    const loaderContainer = document.getElementById("houses-loader-container");
    const loadingSection = document.getElementById("loading-section");

    loaderContainer.classList.remove('hogwarts-mode', 'avatar-mode');
    loadingSection.classList.remove('hogwarts-mode', 'avatar-mode');

    const mode = universe === 'Hogwarts' ? 'hogwarts-mode' : 'avatar-mode';
    loaderContainer.classList.add(mode);
    loadingSection.classList.add(mode);
}

function runSorting() {
    const name = document.getElementById('nameInput').value.trim();
    const sortingUi = document.getElementById('sorting-ui');
    const loadingSection = document.getElementById('loading-section');
    const loaderContainer = document.getElementById('houses-loader-container');

    if (!name) {
        alert("Please enter a name");
        return;
    }

    sortingUi.style.display = "none";
    loadingSection.style.display = "flex";
    loaderContainer.classList.add('loading-active');

    const url = `http://127.0.0.1:8000/sort?name=${encodeURIComponent(name)}&universe=${encodeURIComponent(selectedUniverse)}&user_id=${userId}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            loadingSection.style.display = "none";
            loaderContainer.classList.remove('loading-active');

            if (data.house) {
                // ניקוי תמות קודמות
                Array.from(sortingUi.classList).forEach(cls => {
                    if (cls.startsWith('theme-')) sortingUi.classList.remove(cls);
                });

                let aiResponse = data.house.toLowerCase();
                let cleanHouseName = '';

                // בדיקה לאיזה בית באווטאר זה שייך
                if (aiResponse.includes('fire')) cleanHouseName = 'firenation';
                else if (aiResponse.includes('water')) cleanHouseName = 'watertribe';
                else if (aiResponse.includes('earth')) cleanHouseName = 'earthkingdom';
                else if (aiResponse.includes('air')) cleanHouseName = 'airnomads';
                // בדיקה לאיזה בית בהוגוורטס זה שייך
                else if (aiResponse.includes('gryffindor')) cleanHouseName = 'gryffindor';
                else if (aiResponse.includes('slytherin')) cleanHouseName = 'slytherin';
                else if (aiResponse.includes('ravenclaw')) cleanHouseName = 'ravenclaw';
                else if (aiResponse.includes('hufflepuff')) cleanHouseName = 'hufflepuff';

                // תחילה הוסף את הקלאס — לפני הצגת ה-UI
                if (cleanHouseName !== '') {
                    sortingUi.classList.add(`theme-${cleanHouseName}`);
                }

                // רק אחרי הוספת הקלאס — הצג את ה-UI
                sortingUi.style.display = "flex";
                document.getElementById('input-section').style.display = "none";

                const resultSection = document.getElementById('result-section');
                document.getElementById('result-text').innerText = `${data.name} belongs to ${data.house}!`;
                document.getElementById('reason-text').innerText = data.reason;
                resultSection.style.display = "block";

            } else {
                alert("Error: " + (data.Error || "Unknown error"));
                sortingUi.style.display = "flex";
            }
        })
        .catch((err) => {
            console.error(err);
            loadingSection.style.display = "none";
            sortingUi.style.display = "flex";
            alert("Connection error. Is server.py running?");
        });
}

function resetUI() {
    location.reload();
}