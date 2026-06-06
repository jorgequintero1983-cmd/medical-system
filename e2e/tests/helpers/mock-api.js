/**
 * Mock de respuestas HTTP para pruebas E2E con Playwright.
 */

export async function mockPatientsApi(page, initialPatients = []) {
  const patients = [...initialPatients];

  await page.route("**/patients**", async (route) => {
    const request = route.request();
    const method = request.method();

    if (method === "OPTIONS") {
      await route.fulfill({ status: 200 });
      return;
    }

    if (method === "GET") {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(patients),
      });
      return;
    }

    if (method === "POST") {
      const body = request.postDataJSON();
      const created = {
        id: patients.length + 1,
        document: body.document,
        full_name: body.full_name,
        phone: body.phone,
      };
      patients.push(created);
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(created),
      });
      return;
    }

    await route.continue();
  });
}

export async function mockAuthLogin(page) {
  await page.route("**/auth/login", async (route) => {
    if (route.request().method() === "OPTIONS") {
      await route.fulfill({ status: 200 });
      return;
    }

    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        access_token: "mock-e2e-token",
        token_type: "bearer",
      }),
    });
  });
}
