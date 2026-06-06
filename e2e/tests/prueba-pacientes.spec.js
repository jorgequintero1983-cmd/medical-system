import { expect, test } from "@playwright/test";

test.describe("Prueba E2E - Gestión de pacientes", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
    await page.getByPlaceholder("Correo").fill("admin@test.com");
    await page.getByPlaceholder("Contraseña").fill("123456");
    await page.getByRole("button", { name: "Iniciar sesión" }).click();
    await expect(page.getByText("Panel de Pacientes")).toBeVisible({
      timeout: 15000,
    });
  });

  test("debe mostrar el formulario de crear paciente", async ({ page }) => {
    await expect(page.getByText("Crear Paciente")).toBeVisible();
    await expect(page.getByPlaceholder("Documento")).toBeVisible();
    await expect(page.getByPlaceholder("Nombre completo")).toBeVisible();
    await expect(page.getByPlaceholder("Celular")).toBeVisible();
  });

  test("debe crear un paciente y mostrarlo en la lista", async ({ page }) => {
    page.on("dialog", (dialog) => dialog.accept());

    const documento = String(Date.now()).slice(-10);

    await page.getByPlaceholder("Documento").fill(documento);
    await page.getByPlaceholder("Nombre completo").fill("Paciente E2E");
    await page.getByPlaceholder("Celular").fill("3001234567");
    await page.getByRole("button", { name: "Crear paciente" }).click();

    await expect(page.getByText("Paciente E2E")).toBeVisible({
      timeout: 15000,
    });
  });
});
