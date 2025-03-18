const BASE_URL = "http://localhost:8000";
let token = null;

// Al cargar la página, verificar si el token está en localStorage
document.addEventListener('DOMContentLoaded', () => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
        token = storedToken;
        document.getElementById('loginForm').classList.add('hidden');
        document.getElementById('menu').classList.remove('hidden');
        mostrarSeccion('usuarios');
    }
});

// Evento de inicio de sesión
document.getElementById('loginForm').addEventListener('submit', async function (event) {
    event.preventDefault();
    const userName = document.getElementById('loginUserName').value;
    const password = document.getElementById('loginPassword').value;

    token = await obtenerToken(userName, password);

    if (token) {
        // Guardamos el token en localStorage para persistirlo entre recargas
        localStorage.setItem('token', token);
        document.getElementById('loginForm').classList.add('hidden');
        document.getElementById('menu').classList.remove('hidden');
        mostrarSeccion('usuarios');
    } else {
        document.getElementById('errorMensaje').classList.remove('hidden');
    }
});

// Función para obtener el token de autenticación
async function obtenerToken(userName, password) {
    try {
        const response = await fetch(`${BASE_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ userName, password })
        });

        if (!response.ok) throw new Error("Credenciales incorrectas");

        const data = await response.json();
        return data.token;
    } catch (error) {
        console.error("Error al obtener el token:", error.message);
        return null;
    }
}

// Función para mostrar la sección seleccionada
function mostrarSeccion(seccion) {
    const secciones = document.querySelectorAll(".tab-content");
    secciones.forEach(sec => sec.classList.add("hidden"));

    document.getElementById(seccion).classList.remove("hidden");

    // Resaltar la pestaña activa
    document.querySelectorAll(".tab-button").forEach(btn => btn.classList.remove("active"));
    document.querySelector(`[onclick="mostrarSeccion('${seccion}')"]`).classList.add("active");
}

/* ==========================
       OBTENER USUARIOS
   ========================== */
async function obtenerUsuarios() {
    if (!token) {
        console.error("No se pudo obtener el token");
        return;
    }
    try {
        const response = await fetch(`${BASE_URL}/users/`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) throw new Error("Error al obtener los usuarios");

        const usuarios = await response.json();
        mostrarUsuarios(usuarios);
    } catch (error) {
        console.error(error.message);
    }
}

function mostrarUsuarios(usuarios) {
    const usuariosTabla = document.getElementById("usuariosLista");
    usuariosTabla.innerHTML = ""; // Limpiar contenido previo

    usuarios.forEach(usuario => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${usuario.name}</td>
            <td>${usuario.lastName}</td>
            <td>${usuario.email}</td>
        `;
        usuariosTabla.appendChild(row);
    });
}

// Evento para agregar usuario
document.getElementById('usuarioForm').addEventListener('submit', async function (event) {
    event.preventDefault();
    await agregarUsuario();
});

// Función para agregar usuario
async function agregarUsuario() {
    if (!token) {
        console.error("No tienes un token válido.");
        return;
    }

    const nombre = document.getElementById('nombre').value.trim();
    const apellido = document.getElementById('apellido').value.trim();
    const typeUser = document.getElementById('typeUser').value.trim();
    const userName = document.getElementById('registerUserName').value.trim();
    const email = document.getElementById('registerEmail').value.trim();
    const password = document.getElementById('registerPassword').value.trim();
    const phoneNumber = document.getElementById('phoneNumber').value.trim();
    const status = document.getElementById('status').value.trim();

    // Validar que los campos no estén vacíos
    if (!nombre || !apellido || !typeUser || !userName || !email || !password || !phoneNumber || !status) {
        alert("Todos los campos son obligatorios.");
        return;
    }

    const fechaActual = new Date().toISOString(); // Generar fecha actual en formato ISO

    const usuarioData = {
        name: nombre,
        lastName: apellido,
        typeUser: typeUser,
        userName: userName,
        email: email,
        password: password,
        phoneNumber: phoneNumber,
        status: status,
        registrationDate: fechaActual,
        updateDate: fechaActual
    };

    try {
        const response = await fetch(`${BASE_URL}/users/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(usuarioData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Error al agregar usuario: ${errorData.detail || "Error desconocido"}`);
        }

        console.log("Usuario agregado correctamente.");
        obtenerUsuarios(); // Recargar la lista de usuarios
        document.getElementById('usuarioForm').reset();
    } catch (error) {
        console.error(error.message);
    }
}

/* ==========================
      OBTENER MATERIALES
   ========================== */
async function obtenerMateriales() {
    if (!token) {
        console.error("No se pudo obtener el token");
        return;
    }
    try {
        const response = await fetch(`${BASE_URL}/materials/`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) throw new Error("Error al obtener los materiales");

        const materiales = await response.json();
        mostrarMateriales(materiales);
    } catch (error) {
        console.error(error.message);
    }
}

function mostrarMateriales(materiales) {
    const materialesTabla = document.getElementById("materialesLista");
    materialesTabla.innerHTML = ""; // Limpiar contenido previo

    materiales.forEach(material => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${material.tipo_material}</td>
            <td>${material.marca}</td>
            <td>${material.modelo}</td>
            <td>${material.estado}</td>
        `;
        materialesTabla.appendChild(row);
    });
}

/* ==========================
      AGREGAR MATERIALES
   ========================== */

// Evento para agregar material
document.getElementById('materialForm').addEventListener('submit', async function (event) {
    event.preventDefault();
    await agregarMaterial();
});

// Función para agregar material
async function agregarMaterial() {
    if (!token) {
        console.error("No tienes un token válido.");
        return;
    }

    const tipoMaterial = document.getElementById('tipoMaterial').value.trim();
    const marca = document.getElementById('marca').value.trim();
    const modelo = document.getElementById('modelo').value.trim();
    const estadoMaterial = document.getElementById('estadoMaterial').value.trim();

    // Validar que los campos no estén vacíos
    if (!tipoMaterial || !marca || !modelo || !estadoMaterial) {
        alert("Todos los campos son obligatorios.");
        return;
    }

    const materialData = {
        tipo_material: tipoMaterial,
        marca: marca,
        modelo: modelo,
        estado: estadoMaterial
    };

    try {
        const response = await fetch(`${BASE_URL}/materials/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(materialData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Error al agregar material: ${errorData.detail || "Error desconocido"}`);
        }

        console.log("Material agregado correctamente.");
        obtenerMateriales(); // Recargar la lista de materiales
        document.getElementById('materialForm').reset(); // Limpiar el formulario
    } catch (error) {
        console.error(error.message);
    }
}

/* ==========================
      OBTENER PRÉSTAMOS
   ========================== */
async function obtenerPrestamos() {
    if (!token) {
        console.error("No se pudo obtener el token");
        return;
    }
    try {
        const response = await fetch(`${BASE_URL}/prestamos/`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) throw new Error("Error al obtener los préstamos");

        const prestamos = await response.json();
        mostrarPrestamos(prestamos);
    } catch (error) {
        console.error(error.message);
    }
}

function mostrarPrestamos(prestamos) {
    const prestamosTabla = document.getElementById("prestamosLista");
    prestamosTabla.innerHTML = ""; // Limpiar contenido previo

    prestamos.forEach(prestamo => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${prestamo.id_prestamo}</td>
            <td>${prestamo.id_usuarios}</td>
            <td>${prestamo.id_material}</td>
            <td>${prestamo.fecha_prestamo}</td>
            <td>${prestamo.fecha_devolucion}</td>
            <td>${prestamo.estado_prestamo}</td>
        `;
        prestamosTabla.appendChild(row);
    });
}

/* ==========================
      AGREGAR PRÉSTAMOS
   ========================== */

// Evento para agregar préstamo
document.getElementById('prestamoForm').addEventListener('submit', async function (event) {
    event.preventDefault();
    await agregarPrestamo();
});

// Función para agregar préstamo
async function agregarPrestamo() {
    if (!token) {
        console.error("No tienes un token válido.");
        return;
    }

    const idUsuario = document.getElementById('idUsuario').value.trim();
    const idMaterial = document.getElementById('idMaterial').value.trim();
    const fechaPrestamo = document.getElementById('fechaPrestamo').value.trim();
    const fechaDevolucion = document.getElementById('fechaDevolucion').value.trim();
    const estadoPrestamo = document.getElementById('estadoPrestamo').value.trim();

    // Validar que los campos obligatorios no estén vacíos
    if (!idUsuario || !idMaterial || !fechaPrestamo || !estadoPrestamo) {
        alert("Los campos ID Usuario, ID Material, Fecha Préstamo y Estado son obligatorios.");
        return;
    }

    // Crear el objeto de datos para el préstamo
    const prestamoData = {
        id_usuarios: parseInt(idUsuario), // Convertir a número
        id_material: parseInt(idMaterial), // Convertir a número
        fecha_prestamo: new Date(fechaPrestamo).toISOString(), // Convertir a formato ISO
        fecha_devolucion: fechaDevolucion ? new Date(fechaDevolucion).toISOString() : null, // Puede ser NULL
        estado_prestamo: estadoPrestamo // Estado del préstamo
    };

    try {
        const response = await fetch(`${BASE_URL}/prestamos/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(prestamoData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.log(errorData);
            throw new Error(`Error al agregar préstamo: ${errorData.detail || "Error desconocido"}`);
        }

        console.log("Préstamo agregado correctamente.");
        obtenerPrestamos(); // Recargar la lista de préstamos
        document.getElementById('prestamoForm').reset(); // Limpiar el formulario
    } catch (error) {
        console.error(error.message);
    }
}

// Función de logout (cerrar sesión)
function cerrarSesion() {
    // Eliminar el token del localStorage
    localStorage.removeItem('token');
    token = null;

    // Volver al formulario de login y ocultar el menú
    document.getElementById('loginForm').classList.remove('hidden');
    document.getElementById('menu').classList.add('hidden');

    // Limpiar el contenido de las secciones
    document.querySelectorAll('.tab-content').forEach(sec => sec.classList.add('hidden'));
}