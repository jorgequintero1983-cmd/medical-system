import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [patients, setPatients] = useState([]);

  const [document, setDocument] = useState("");
  const [fullName, setFullName] = useState("");
  const [phone, setPhone] = useState("");

  const [editingId, setEditingId] = useState(null);

  const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const login = async () => {
  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/auth/login",
      {
        email,
        password,
      }
    );

    localStorage.setItem(
      "token",
      response.data.access_token
    );

    setToken(response.data.access_token);

    // Entrar directamente al Dashboard
    loadPatients();

  } catch (error) {
    console.log(error);
    alert("Error de login");
  }
};

  const loadPatients = async () => {
    try {
      const response = await api.get("/patients");
      setPatients(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    if (token) {
      loadPatients();
    }
  }, [token]);

  const createPatient = async () => {
  try {
    await api.post("/patients", {
      document,
      full_name: fullName,
      phone,
    });

    setDocument("");
    setFullName("");
    setPhone("");

    loadPatients();

    alert("Paciente creado correctamente");
  } catch (error) {

    console.log(error);

    if (error.response?.data?.detail) {

  const detail = error.response.data.detail;

  if (Array.isArray(detail)) {
    alert(
      detail
        .map((e) => e.msg)
        .join("\n")
    );
  } else {
    alert(detail);
  }

} else {
      alert("Error creando paciente, no puede tener espacios en blanco");
    }

  }
};

  const deletePatient = async (id) => {
    try {
      await api.delete(`/patients/${id}`);

      loadPatients();

      alert("Paciente eliminado");
    } catch (error) {
      console.log(error);
      alert("Error eliminando paciente");
    }
  };

  const editPatient = (patient) => {
    setEditingId(patient.id);

    setDocument(patient.document);
    setFullName(patient.full_name);
    setPhone(patient.phone);
  };

  const updatePatient = async () => {
    try {
      await api.put(`/patients/${editingId}`, {
        document,
        full_name: fullName,
        phone,
      });

      setEditingId(null);

      setDocument("");
      setFullName("");
      setPhone("");

      loadPatients();

      alert("Paciente actualizado");
    } catch (error) {
      console.log(error);
      alert("Error actualizando paciente");
    }
  };

  const logout = () => {
    localStorage.removeItem("token");

    setToken(null);

    setEmail("");
    setPassword("");
  };

  if (!token) {
    return (
      <div
        style={{
          background: "#eef2f7",
          minHeight: "100vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: "100px",
        }}
      >
        <div>
          <h1
            style={{
              fontSize: "80px",
              color: "#07122F",
            }}
          >
            Sistema Médico
          </h1>

          <p
            style={{
              fontSize: "20px",
              color: "#5c6b82",
            }}
          >
            Plataforma de Gestión de Pacientes
          </p>
        </div>

        <div
          style={{
            background: "white",
            padding: "40px",
            borderRadius: "20px",
            width: "400px",
          }}
        >
          <h1
            style={{
              fontSize: "60px",
              marginBottom: "30px",
              color: "#07122F",
            }}
          >
            Iniciar sesión
          </h1>

          <input
            type="email"
            placeholder="Correo"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={inputStyle}
          />

          <input
            type="password"
            placeholder="Contraseña"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={inputStyle}
          />

          <button onClick={login} style={buttonStyle}>
            Iniciar sesión
          </button>
        </div>
      </div>
    );
  }

  return (
    <div
      style={{
        background: "#eef2f7",
        minHeight: "100vh",
      }}
    >
      <div
        style={{
          background: "#07122F",
          color: "white",
          padding: "20px",
          display: "flex",
          justifyContent: "space-between",
        }}
      >
        <h1>Sistema Médico</h1>

        <button
          onClick={logout}
          style={{
            background: "#ff4d4d",
            border: "none",
            color: "white",
            padding: "10px 20px",
            borderRadius: "10px",
            cursor: "pointer",
          }}
        >
          Cerrar sesión
        </button>
      </div>

      <div style={{ padding: "30px" }}>
        <h2>Panel de Pacientes</h2>

        <div
          style={{
            background: "white",
            padding: "20px",
            borderRadius: "20px",
            marginTop: "20px",
          }}
        >
          <h3>
            {editingId ? "Editar Paciente" : "Crear Paciente"}
          </h3>

          <input
            type="text"
            placeholder="Documento"
            value={document}
            onChange={(e) => setDocument(
              e.target.value.replace(/\D/g, "")
            )}
            style={inputStyle}
          />

          <input
            type="text"
            placeholder="Nombre completo"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            style={inputStyle}
          />

          <input
            type="text"
            placeholder="Celular"
            value={phone}
            onChange={(e) => setPhone(
              e.target.value.replace(/\D/g, ""))
            }
            style={inputStyle}
          />

          {editingId ? (
            <button onClick={updatePatient} style={buttonStyle}>
              Actualizar paciente
            </button>
          ) : (
            <button onClick={createPatient} style={buttonStyle}>
              Crear paciente
            </button>
          )}
        </div>

        <div
          style={{
            background: "white",
            padding: "20px",
            borderRadius: "20px",
            marginTop: "40px",
          }}
        >
          <h3>Lista de Pacientes</h3>

          <table
            width="100%"
            style={{
              marginTop: "20px",
              borderCollapse: "collapse",
            }}
          >
            <thead>
              <tr
                style={{
                  background: "#dbe3ef",
                  textAlign: "left",
                }}
              >
                <th style={thStyle}>ID</th>
                <th style={thStyle}>Documento</th>
                <th style={thStyle}>Nombre</th>
                <th style={thStyle}>Celular</th>
                <th style={thStyle}>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {patients.map((patient) => (
                <tr key={patient.id}>
                  <td style={tdStyle}>{patient.id}</td>
                  <td style={tdStyle}>{patient.document}</td>
                  <td style={tdStyle}>{patient.full_name}</td>
                  <td style={tdStyle}>{patient.phone}</td>

                  <td style={tdStyle}>
                    <button
                      onClick={() => editPatient(patient)}
                      style={{
                        background: "#2563eb",
                        color: "white",
                        border: "none",
                        padding: "10px",
                        borderRadius: "10px",
                        marginRight: "10px",
                        cursor: "pointer",
                      }}
                    >
                      Editar
                    </button>

                    <button
                      onClick={() => deletePatient(patient.id)}
                      style={{
                        background: "#ff4d4d",
                        color: "white",
                        border: "none",
                        padding: "10px",
                        borderRadius: "10px",
                        cursor: "pointer",
                      }}
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

const inputStyle = {
  width: "100%",
  padding: "15px",
  marginTop: "20px",
  borderRadius: "10px",
  border: "1px solid #ccc",
};

const buttonStyle = {
  width: "100%",
  padding: "15px",
  marginTop: "20px",
  background: "#2563eb",
  color: "white",
  border: "none",
  borderRadius: "10px",
  cursor: "pointer",
};

const thStyle = {
  padding: "15px",
};

const tdStyle = {
  padding: "15px",
  borderBottom: "1px solid #ddd",
};

export default App;