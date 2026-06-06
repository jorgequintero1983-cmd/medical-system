import { expect, test } from "@playwright/test";
import { mockAuthLogin, mockPatientsApi } from "./helpers/mock-api.js";

test.describe("Prueba E2E - Pacientes con API mockeada", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthLogin(page);
    await mockPatientsApi(page);
    await page.goto("/");
    await page.getByPlaceholder("Correo").fill("admin@test.com");
    await page.getByPlaceholder("Contraseña").fill("123456");
    await page.getByRole("button", { name: "Iniciar sesión" }).click();
    await expect(page.getByText("Panel de Pacientes")).toBeVisible({
      timeout: 15000,
    });
  });

  test("debe crear un paciente usando respuestas mockeadas", async ({ page }) => {
    page.on("dialog", (dialog) => dialog.accept());

    const documento = String(Date.now()).slice(-10);

    await page.getByPlaceholder("Documento").fill(documento);
    await page.getByPlaceholder("Nombre completo").fill("Paciente Mock E2E");
    await page.getByPlaceholder("Celular").fill("3001234567");
    await page.getByRole("button", { name: "Crear paciente" }).click();

    await expect(page.getByText("Paciente Mock E2E")).toBeVisible({
      timeout: 15000,
    });
  });
});
