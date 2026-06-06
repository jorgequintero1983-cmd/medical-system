import { expect, test } from "@playwright/test";

test.describe("Prueba E2E - Inicio de sesión", () => {
  test("debe iniciar sesión y mostrar el panel de pacientes", async ({
    page,
  }) => {
    await page.goto("/");

    await expect(page.getByPlaceholder("Correo")).toBeVisible();
    await page.getByPlaceholder("Correo").fill("admin@test.com");
    await page.getByPlaceholder("Contraseña").fill("123456");
    await page.getByRole("button", { name: "Iniciar sesión" }).click();

    await expect(page.getByText("Panel de Pacientes")).toBeVisible({
      timeout: 15000,
    });
    await expect(page.getByRole("button", { name: "Cerrar sesión" })).toBeVisible();
  });

  test("debe mostrar error con credenciales inválidas", async ({ page }) => {
    page.on("dialog", (dialog) => dialog.accept());

    await page.goto("/");
    await page.getByPlaceholder("Correo").fill("noexiste@test.com");
    await page.getByPlaceholder("Contraseña").fill("wrong");
    await page.getByRole("button", { name: "Iniciar sesión" }).click();

    await expect(page.getByPlaceholder("Correo")).toBeVisible();
    await expect(page.getByText("Panel de Pacientes")).not.toBeVisible();
  });
});
