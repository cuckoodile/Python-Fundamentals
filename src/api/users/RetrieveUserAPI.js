import BASE_DIR from "../config.js";

export default async function RetrieveUserAPI(id) {
  const response = await fetch(`${BASE_DIR}/users/${id}/`);
  const data = await response.json();

  console.log(data)
  if (response.ok) {
    return data;
  } else {
    throw new Error("Something went Wrong!", data.detail);
  }
}

// RetrieveUserAPI(7)
