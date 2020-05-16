let postContent = document.getElementsByClassName('post-container')[0];
let images = document.querySelectorAll('.post-container img');
for (let i = 0; i < images.length; i++) {
    let image = images[i];
    image.classList.add("img-fluid");
}
