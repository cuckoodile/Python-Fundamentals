import BASE_DIR from "../config.js";

export default async function CreateUserAPI(formData) {
  const response = await fetch(`${BASE_DIR}/users/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });

  const data = await response.json();

  console.log(data);

  if (response.ok) {
    return data;
  } else {
    throw new Error("Something went wrong!");
  }
}
