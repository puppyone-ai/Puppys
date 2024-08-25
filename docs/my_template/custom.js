document.addEventListener("DOMContentLoaded", function() {
    const nav = document.querySelector("nav");

    if (nav) {
        const watermark = document.createElement("li");
        watermark.innerHTML = '<a href="https://your-company-url.com" target="_blank">Powered by YourCompany</a>';
        watermark.style.marginTop = "20px";  // 添加一些间距
        watermark.style.fontStyle = "italic"; // 斜体

        nav.appendChild(watermark);
    }
});
