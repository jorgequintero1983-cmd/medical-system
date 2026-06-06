import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import axios from "axios";
import App from "../App";

vi.mock("axios");

const mockApiGet = vi.fn();
const mockApiPost = vi.fn();
const mockApiPut = vi.fn();
const mockApiDelete = vi.fn();

const samplePatient = {
  id: 1,
  document: "1234567890",
  full_name: "Juan Pérez",
  phone: "3001234567",
};

function setupApiMock() {
  axios.create.mockReturnValue({
    get: mockApiGet,
    post: mockApiPost,
    put: mockApiPut,
    delete: mockApiDelete,
  });
}

function renderWithToken(patients = []) {
  localStorage.setItem("token", "fake-token");
  mockApiGet.mockResolvedValue({ data: patients });
  render(<App />);
}

describe("Prueba de Componentes - Login", () => {
  beforeEach(() => {
    localStorage.clear();
    vi.clearAllMocks();
    setupApiMock();
    vi.spyOn(window, "alert").mockImplementation(() => {});
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("muestra el formulario de login sin token", () => {
    render(<App />);

    expect(screen.getByPlaceholderText("Correo")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Contraseña")).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Iniciar sesión" })
    ).toBeInTheDocument();
  });

  test("inicia sesión correctamente y muestra el panel", async () => {
    axios.post.mockResolvedValueOnce({
      data: { access_token: "nuevo-token" },
    });
    mockApiGet.mockResolvedValue({ data: [samplePatient] });

    render(<App />);

    fireEvent.change(screen.getByPlaceholderText("Correo"), {
      target: { value: "admin@test.com" },
    });
    fireEvent.change(screen.getByPlaceholderText("Contraseña"), {
      target: { value: "123456" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Iniciar sesión" }));

    await waitFor(() => {
      expect(screen.getByText("Panel de Pacientes")).toBeInTheDocument();
    });

    expect(localStorage.getItem("token")).toBe("nuevo-token");
    expect(axios.post).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/auth/login",
      { email: "admin@test.com", password: "123456" }
    );
  });

  test("muestra alerta cuando el login falla", async () => {
    axios.post.mockRejectedValueOnce(new Error("Credenciales inválidas"));

    render(<App />);

    fireEvent.click(screen.getByRole("button", { name: "Iniciar sesión" }));

    await waitFor(() => {
      expect(window.alert).toHaveBeenCalledWith("Error de login");
    });
  });
});

describe("Prueba de Componentes - Panel de Pacientes", () => {
  beforeEach(() => {
    localStorage.clear();
    vi.clearAllMocks();
    setupApiMock();
    vi.spyOn(window, "alert").mockImplementation(() => {});
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("carga y muestra la lista de pacientes", async () => {
    renderWithToken([samplePatient]);

    await waitFor(() => {
      expect(screen.getByText("Juan Pérez")).toBeInTheDocument();
    });

    expect(screen.getByText("1234567890")).toBeInTheDocument();
    expect(mockApiGet).toHaveBeenCalledWith("/patients");
  });

  test("cierra sesión y vuelve al login", async () => {
    renderWithToken([samplePatient]);

    await waitFor(() => {
      expect(screen.getByText("Panel de Pacientes")).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole("button", { name: "Cerrar sesión" }));

    expect(localStorage.getItem("token")).toBeNull();
    expect(screen.getByPlaceholderText("Correo")).toBeInTheDocument();
  });

  test("crea un paciente correctamente", async () => {
    mockApiGet.mockResolvedValue({ data: [] });
    mockApiPost.mockResolvedValueOnce({ data: samplePatient });

    renderWithToken();

    await waitFor(() => {
      expect(screen.getByText("Crear Paciente")).toBeInTheDocument();
    });

    fireEvent.change(screen.getByPlaceholderText("Documento"), {
      target: { value: "1234567890" },
    });
    fireEvent.change(screen.getByPlaceholderText("Nombre completo"), {
      target: { value: "Juan Pérez" },
    });
    fireEvent.change(screen.getByPlaceholderText("Celular"), {
      target: { value: "3001234567" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Crear paciente" }));

    await waitFor(() => {
      expect(mockApiPost).toHaveBeenCalledWith("/patients", {
        document: "1234567890",
        full_name: "Juan Pérez",
        phone: "3001234567",
      });
    });

    expect(window.alert).toHaveBeenCalledWith("Paciente creado correctamente");
  });

  test("filtra caracteres no numéricos en documento y celular", async () => {
    renderWithToken();

    await waitFor(() => {
      expect(screen.getByPlaceholderText("Documento")).toBeInTheDocument();
    });

    fireEvent.change(screen.getByPlaceholderText("Documento"), {
      target: { value: "12abc34" },
    });
    fireEvent.change(screen.getByPlaceholderText("Celular"), {
      target: { value: "30x0y1" },
    });

    expect(screen.getByPlaceholderText("Documento")).toHaveValue("1234");
    expect(screen.getByPlaceholderText("Celular")).toHaveValue("3001");
  });

  test("muestra errores de validación al crear paciente", async () => {
    mockApiPost.mockRejectedValueOnce({
      response: {
        data: {
          detail: [{ msg: "Documento inválido" }],
        },
      },
    });

    renderWithToken();

    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Crear paciente" })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole("button", { name: "Crear paciente" }));

    await waitFor(() => {
      expect(window.alert).toHaveBeenCalledWith("Documento inválido");
    });
  });

  test("muestra error string al crear paciente duplicado", async () => {
    mockApiPost.mockRejectedValueOnce({
      response: {
        data: {
          detail: "Paciente ya existe",
        },
      },
    });

    renderWithToken();

    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Crear paciente" })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole("button", { name: "Crear paciente" }));

    await waitFor(() => {
      expect(window.alert).toHaveBeenCalledWith("Paciente ya existe");
    });
  });

  test("muestra error genérico al crear paciente", async () => {
    mockApiPost.mockRejectedValueOnce(new Error("Network error"));

    renderWithToken();

    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Crear paciente" })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole("button", { name: "Crear paciente" }));

    await waitFor(() => {
      expect(window.alert).toHaveBeenCalledWith(
        "Error creando paciente, no puede tener espacios en blanco"
      );
    });
  });

  test("edita y actualiza un paciente", async () => {
    mockApiPut.mockResolvedValueOnce({ data: samplePatient });

    renderWithToken([samplePatient]);

    await waitFor(() => {
      expect(screen.getByText("Juan Pérez")).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole("button", { name: "Editar" }));

    expect(screen.getByText("Editar Paciente")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Documento")).toHaveValue("1234567890");

    fireEvent.change(screen.getByPlaceholderText("Nombre completo"), {
      target: { value: "Juan Actualizado" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Actualizar paciente" }));

    await waitFor(() => {
      expect(mockApiPut).toHaveBeenCalledWith("/patients/1", {
        document: "1234567890",
        full_name: "Juan Actualizado",
        phone: "3001234567",
      });
    });

    expect(window.alert).toHaveBeenCalledWith("Paciente actualizado");
  });

  test("muestra error al actualizar paciente", async () => {
    mockApiPut.mockRejectedValueOnce(new Error("Update failed"));

    renderWithToken([samplePatient]);

    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Editar" })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole("button", { name: "Editar" }));
    fireEvent.click(screen.getByRole("button", { name: "Actualizar paciente" }));

    await waitFor(() => {
      expect(window.alert).toHaveBeenCalledWith("Error actualizando paciente");
    });
  });

  test("elimina un paciente", async () => {
    mockApiDelete.mockResolvedValueOnce({ data: {} });

    renderWithToken([samplePatient]);

    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Eliminar" })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole("button", { name: "Eliminar" }));

    await waitFor(() => {
      expect(mockApiDelete).toHaveBeenCalledWith("/patients/1");
    });

    expect(window.alert).toHaveBeenCalledWith("Paciente eliminado");
  });

  test("no falla si la carga de pacientes tiene error", async () => {
    mockApiGet.mockRejectedValueOnce(new Error("Load failed"));

    renderWithToken();

    await waitFor(() => {
      expect(mockApiGet).toHaveBeenCalledWith("/patients");
    });

    expect(screen.getByText("Panel de Pacientes")).toBeInTheDocument();
  });

  test("muestra error al eliminar paciente", async () => {
    mockApiDelete.mockRejectedValueOnce(new Error("Delete failed"));

    renderWithToken([samplePatient]);

    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Eliminar" })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole("button", { name: "Eliminar" }));

    await waitFor(() => {
      expect(window.alert).toHaveBeenCalledWith("Error eliminando paciente");
    });
  });
});
