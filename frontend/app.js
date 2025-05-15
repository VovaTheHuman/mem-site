const API_URL = "http://localhost:8000";

document.getElementById("memeForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = document.getElementById("title").value;
    const image_url = document.getElementById("image_url").value;
    const category = document.getElementById("category").value;

    const response = await fetch(`${API_URL}/memes`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ title, image_url, category })
    });

    if (response.ok) {
        alert("Мем додано!");
        document.getElementById("memeForm").reset();
        loadMemes();
    } else {
        alert("Помилка при додаванні мему.");
    }
});

document.getElementById("loadMemesBtn").addEventListener("click", loadMemes);

async function loadMemes() {
    const response = await fetch(`${API_URL}/memes`);
    const memes = await response.json();

    const gallery = document.getElementById("memesGallery");
    gallery.innerHTML = "";

    memes.forEach(meme => {
        const div = document.createElement("div");
        div.id = "meme";
        div.innerHTML = `
            <h3>${meme.title}</h3>
            <img src="${meme.image_url}" alt="meme">
            <p><strong>Категорія:</strong> ${meme.category}</p>
            <p><small>${new Date(meme.created_at).toLocaleString()}</small></p>
        `;
        gallery.appendChild(div);
    });
}
