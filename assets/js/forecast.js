// Load timestamp and refresh images
fetch('/files/forecast_metadata.json')
  .then(r => r.json())
  .then(data => {
    if (data && data.timestamp) {
      const d = new Date(data.timestamp);
      if (isFinite(d)) {
        const el = document.getElementById('last-updated');
        if (el) el.textContent = d.toLocaleString();
      }
    }
  })
  .catch(e => console.error('Timestamp error:', e));

// Cache bust images on load
window.addEventListener('load', function() {
  const t = new Date().getTime();
  const imgs = ['forecast-plot-katoomba', 'forecast-plot-nowra'];
  imgs.forEach(id => {
    const img = document.getElementById(id);
    if (img) {
      img.src = img.src.split('?')[0] + '?t=' + t;
    }
  });
});
