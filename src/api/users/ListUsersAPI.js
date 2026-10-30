import BASE_DIR from "../config.js";

export default async function ListUsersAPI() {
  const response = await fetch(`${BASE_DIR}/users/`);
  const data = await response.json();

  if (response.ok) {
    return data;
  } else {
    throw new Error("Something went Wrong!", data.detail);
  }
}

ListUsersAPI();
