import { render, screen } from "@testing-library/react";
import axios from "axios";
import App from "../App";

vi.mock("axios");

const mockApiGet = vi.fn();
const mockApiPost = vi.fn();

describe("Prueba de Componentes - Login", () => {
  beforeEach(() => {
    localStorage.clear();
    vi.clearAllMocks();
    axios.create.mockReturnValue({
      get: mockApiGet,
      post: mockApiPost,
    });
  });

  test("Debe mostrar formulario login", () => {
    render(<App />);

    expect(screen.getByPlaceholderText("Correo")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Contraseña")).toBeInTheDocument();
    expect(mockApiGet).not.toHaveBeenCalled();
  });

  test("Debe mostrar botón iniciar sesión", () => {
    render(<App />);

    expect(
      screen.getByRole("button", {
        name: "Iniciar sesión",
      }),
    ).toBeInTheDocument();
    expect(mockApiPost).not.toHaveBeenCalled();
  });
});
