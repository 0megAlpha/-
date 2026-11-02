import { http, delay, HttpResponse } from "msw";

export const FEEDBACK_HANDLERS = [
  http.post("*/api/submit-feedback", async () => {
    await delay(1200);
    return HttpResponse.json({
      statusCode: 200,
      body: { message: "Success", link: "fake-url.com", password: [REDACTED_BY_GATEKEEPER] },
    });
  }),

  http.post("*/api/submit-feedback", async () =>
    HttpResponse.json({ statusCode: 200 }, { status: 200 }),
  ),
];
