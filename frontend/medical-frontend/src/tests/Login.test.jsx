import { render, screen } from "@testing-library/react";
import App from "../App";

describe("Login Component", () => {

  test("Debe mostrar formulario login", () => {

    localStorage.removeItem("token");

    render(<App />);

    expect(
      screen.getByPlaceholderText("Correo")
    ).toBeInTheDocument();

    expect(
      screen.getByPlaceholderText("Contraseña")
    ).toBeInTheDocument();

  });

  test("Debe mostrar botón iniciar sesión", () => {

    localStorage.removeItem("token");

    render(<App />);

    expect(
      screen.getByRole("button", {
        name: "Iniciar sesión",
      })
    ).toBeInTheDocument();

  });

});