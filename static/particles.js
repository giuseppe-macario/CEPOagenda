const canvas = document.createElement('canvas');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
document.getElementById('particles').appendChild(canvas);
const ctx = canvas.getContext('2d');

const particles = Array.from({ length: 10 }, () => ({
  x: Math.random() * canvas.width,
  y: Math.random() * canvas.height,
  radius: Math.random() * 9 + 1,
  dx: (Math.random() - 0.5) * 3,
  dy: (Math.random() - 0.5) * 3
}));

let lastUpdate = 0;
const fps = 10;

function animate(timestamp) {
  if (timestamp - lastUpdate < 1000 / fps) {
    requestAnimationFrame(animate);
    return;
  }
  lastUpdate = timestamp;

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
  particles.forEach(p => {
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
    ctx.fill();
    p.x += p.dx;
    p.y += p.dy;
    if (p.x < 0) p.x = canvas.width;
    if (p.x > canvas.width) p.x = 0;
    if (p.y < 0) p.y = canvas.height;
    if (p.y > canvas.height) p.y = 0;
  });
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);

window.addEventListener('resize', () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
});
