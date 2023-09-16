document.querySelector('form').addEventListener('submit', function (e) {
    e.preventDefault();
    const fileInput = document.querySelector('input[type="file"]');
    const passwordInput = document.querySelector('input[type="password"]');
    const pdfContainer = document.getElementById('pdfContainer');
    
    const formData = new FormData();
    formData.append('pdfFile', fileInput.files[0]);
    formData.append('password', passwordInput.value);
    
    fetch('unlock.php', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        const objectURL = URL.createObjectURL(blob);
        const embed = document.createElement('embed');
        embed.src = objectURL;
        embed.type = 'application/pdf';
        embed.width = '100%';
        embed.height = '600px';
        pdfContainer.innerHTML = '';
        pdfContainer.appendChild(embed);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
