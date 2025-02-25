document.getElementById("fetch-btn").addEventListener("click", fetchRandomAchievement);

async function fetchRandomAchievement() {
    const wikiUrl = "https://dungeoncrawlercarl.fandom.com/api.php";
    const pageName = "Achievements";

    try {
        // Step 1: Fetch the Achievements page
        let response = await fetch(`${wikiUrl}?action=parse&page=${pageName}&format=json&origin=*`);
        let data = await response.json();
        
        // Step 2: Extract the HTML content
        let htmlContent = data.parse.text["*"];
        
        // Step 3: Convert HTML string into a DOM object
        let parser = new DOMParser();
        let doc = parser.parseFromString(htmlContent, "text/html");

        // Step 4: Find all achievement entries (assuming they are in a list or table)
        let achievementElements = doc.querySelectorAll("li");  // Change if achievements are in a table
        
        if (achievementElements.length === 0) {
            document.getElementById("content").innerText = "No achievements found.";
            return;
        }

        // Step 5: Select a random achievement
        let randomIndex = Math.floor(Math.random() * achievementElements.length);
        let achievement = achievementElements[randomIndex];

        // Extract title and description
        let title = achievement.querySelector("b")?.innerText || "Unknown Achievement";
        let description = achievement.innerText.replace(title, "").trim();

        // Step 6: Update the page
        document.getElementById("title").innerText = title;
        document.getElementById("content").innerText = description;
        document.getElementById("source-link").href = `https://dungeoncrawlercarl.fandom.com/wiki/${pageName}`;
        document.getElementById("source-link").innerText = "See all achievements";
    } catch (error) {
        console.error("Error fetching achievement:", error);
        document.getElementById("content").innerText = "Oops! Something went wrong.";
    }
}

// Load an achievement on page load
fetchRandomAchievement();
