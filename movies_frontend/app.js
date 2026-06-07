const API_URL = "http://127.0.0.1:8000/v1/movies/";

// Elementos de la interfaz
const movieForm = document.getElementById("movieForm");
const updateForm = document.getElementById("updateForm");
const moviesList = document.getElementById("moviesList");
const btnRefresh = document.getElementById("btnRefresh");

// 1. MOSTRAR (GET): Obtener y renderizar las películas
async function fetchMovies() {
    try {
        const response = await fetch(API_URL);
        const movies = await response.json();
        
        moviesList.innerHTML = "";
        
        if (movies.length === 0) {
            moviesList.innerHTML = "<p style='color: #bdc3c7;'>No movies in the database.</p>";
            return;
        }

        movies.forEach(movie => {
            const movieRow = document.createElement("div");
            movieRow.className = "movie-row";
            movieRow.innerHTML = `
                <div class="movie-info">
                    <h4><span class="movie-id-badge">ID: ${movie.id}</span> ${movie.title}</h4>
                    <p>${movie.description || "Without description"}</p>
                </div>
                <div>
                    <button class="btn-delete" onclick="deleteMovie(${movie.id})">🗑️ Delete</button>
                </div>
            `;
            moviesList.appendChild(movieRow);
        });
    } catch (error) {
        console.error("Error:", error);
        moviesList.innerHTML = "<p style='color: #ef233c;'>Connection error with Backend API.</p>";
    }
}

// 2. GUARDAR (POST): Insertar nueva película
movieForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, description })
        });

        if (response.ok) {
            movieForm.reset();
            fetchMovies(); // Recarga automáticamente la lista
        }
    } catch (error) {
        console.error("Error creating movie:", error);
    }
});

// 3. ACTUALIZAR (PUT): Modificar película existente por su ID
updateForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const id = document.getElementById("updateId").value;
    const title = document.getElementById("updateTitle").value;
    const description = document.getElementById("updateDescription").value;

    try {
        const response = await fetch(`${API_URL}${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, description })
        });

        if (response.ok) {
            updateForm.reset();
            fetchMovies(); // Recarga automáticamente la lista
        } else {
            alert("Movie ID not found.");
        }
    } catch (error) {
        console.error("Error updating movie:", error);
    }
});

// 4. ELIMINAR (DELETE): Borrar película de la base de datos
async function deleteMovie(id) {
    if (confirm(`Are you sure you want to delete movie with ID: ${id}?`)) {
        try {
            const response = await fetch(`${API_URL}${id}`, {
                method: "DELETE"
            });
            if (response.ok) {
                fetchMovies(); // Recarga automáticamente la lista
            }
        } catch (error) {
            console.error("Error deleting movie:", error);
        }
    }
}

// Botón manual de Mostrar / Refrescar
btnRefresh.addEventListener("click", fetchMovies);

// Cargar la lista automáticamente al abrir el archivo
document.addEventListener("DOMContentLoaded", fetchMovies);