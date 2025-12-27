const menus = [
    {id: 1, n: 'Rendang', p: 25000, b: true, img: 'https://images.unsplash.com/photo-1626776876729-bab4e2233170?w=500&auto=format&fit=crop&q=60'},
    {id: 2, n: 'Ayam Pop', p: 22000, b: true, img: 'https://images.unsplash.com/photo-1626074353765-517a681e40be?w=500&auto=format&fit=crop&q=60'},
    {id: 3, n: 'Teh Talua', p: 12000, b: false, img: 'https://images.unsplash.com/photo-1544782707-160a2b005370?w=500&auto=format&fit=crop&q=60'}
];

let userActive = null;
let authMode = 'login';
let currentItem = {};
let selectedTable = null;

// Generate Tampilan Menu
function renderMenu() {
    const bestSellerList = document.getElementById('best-seller-list');
    const allMenuList = document.getElementById('all-menu-list');

    menus.forEach(m => {
        const card = `
            <div class="col-md-4">
                <div class="card card-menu shadow-sm">
                    <img src="${m.img}" class="card-img-top" style="height:200px; object-fit:cover;">
                    <div class="card-body text-center">
                        <h5 class="fw-bold">${m.n}</h5>
                        <p class="text-danger fw-bold">Rp ${m.p.toLocaleString()}</p>
                        <button class="btn btn-danger btn-sm rounded-pill px-4" onclick="preCheckout('${m.n}', ${m.p})">Pesan</button>
                    </div>
                </div>
            </div>`;
        if(m.b) bestSellerList.innerHTML += card;
        allMenuList.innerHTML += card;
    });
}

// Munculkan/Sembunyikan Pilihan Meja
function toggleTableSelection() {
    const type = document.getElementById('type').value;
    const tableArea = document.getElementById('table-area');
    if (type === 'Dine-in') {
        tableArea.style.display = 'block';
        renderTables();
    } else {
        tableArea.style.display = 'none';
        selectedTable = null;
    }
}

// Generate Pilihan Meja (1-12)
function renderTables() {
    const container = document.getElementById('table-selection');
    container.innerHTML = '';
    for (let i = 1; i <= 12; i++) {
        container.innerHTML += `
            <input type="radio" class="btn-check" name="btnradio" id="meja${i}" autocomplete="off">
            <label class="btn btn-outline-danger btn-sm" for="meja${i}" onclick="selectedTable=${i}">Meja ${i}</label>
        `;
    }
}

// Logika Login/Register
function toggleAuthMode() {
    authMode = (authMode === 'login') ? 'register' : 'login';
    document.getElementById('modalTitle').innerText = (authMode === 'login') ? 'Masuk' : 'Daftar Akun Baru';
}

async function handleAuth() {
    const userVal = document.getElementById('username').value;
    const passVal = document.getElementById('password').value;
    if(!userVal || !passVal) return alert("Isi data dengan lengkap!");

    const url = authMode === 'login' ? '/api/login' : '/api/register';
    
    // Simulasi Fetch ke Backend
    try {
        const res = await fetch(url, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username: userVal, password: passVal})
        });
        const data = await res.json();
        if(data.success) {
            userActive = data.user;
            document.getElementById('auth-section').innerHTML = `<span class="badge bg-light text-dark p-2">Halo, ${userActive}</span>`;
            bootstrap.Modal.getInstance(document.getElementById('loginModal')).hide();
        } else alert(data.msg);
    } catch(e) {
        // Fallback jika belum ada Flask (untuk demo)
        userActive = userVal;
        document.getElementById('auth-section').innerHTML = `<span class="badge bg-light text-dark p-2">Halo, ${userActive}</span>`;
        bootstrap.Modal.getInstance(document.getElementById('loginModal')).hide();
    }
}

// Buka Modal Pesanan
function preCheckout(nama, harga) {
    if(!userActive) return alert("Silakan Login Terlebih Dahulu!");
    currentItem = {nama, harga};
    document.getElementById('orderDetail').innerHTML = `Item: <b>${nama}</b><br>Harga: <b>Rp ${harga.toLocaleString()}</b>`;
    document.getElementById('type').value = 'Takeaway';
    document.getElementById('table-area').style.display = 'none';
    new bootstrap.Modal(document.getElementById('checkoutModal')).show();
}

// Kirim Pesanan Akhir
async function submitOrder() {
    const type = document.getElementById('type').value;
    const date = document.getElementById('date').value;

    if(!date) return alert("Pilih tanggal dan waktu!");
    if(type === 'Dine-in' && !selectedTable) return alert("Pilih nomor meja!");

    const payload = {
        username: userActive,
        item: currentItem.nama,
        method: type,
        table: selectedTable,
        booking_time: date
    };

    console.log("Mengirim Pesanan:", payload);

    try {
        const res = await fetch('/api/order', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        alert(data.msg);
    } catch(e) {
        alert("Ondeh Mande! Pesanan Berhasil (Simulasi: Server belum terhubung)");
    }
    location.reload();
}

renderMenu();