import React from "react";
import { useState } from "react";
import CreateUserAPI from "../api/users/CreateUserAPI";

export default function FormPupop({ setVisible }) {
  const [formData, setFormData] = useState({});

  function handeInputChange(e) {
    const { name, value } = e.target;

    setFormData({ ...formData, [name]: value });
  }

  function handleImage(e) {
    const file = e.target.files[0];

    setFormData({
      ...formData,
      profile: file,
      showProfile: URL.createObjectURL(file),
    });
  }

  function handleFormSubmit(e) {
    e.preventDefault();

    console.log("Submit: ", formData);

    CreateUserAPI(formData)
      .then((data) => [alert("Success!"), console.log(data)])
      .catch(() => alert("Something went wrong"));
  }

  return (
    <div className="h-screen w-screen bg-black/80 backdrop-blur-sm fixed top-0 left-0 flex justify-center items-center">
      <form
        onSubmit={handleFormSubmit}
        className="bg-white text-black rounded-lg p-5 flex flex-col gap-10"
      >
        {/* Title */}
        <h1>Create New User</h1>

        {/* Input Fields */}
        <section>
          {/* Username Field */}
          <div>
            <label htmlFor="username">Username</label>
            <input
              type="text"
              name="username"
              id="username"
              value={formData.username}
              onChange={handeInputChange}
            />
          </div>

          {/* Password Field */}
          <div>
            <label htmlFor="password">Password</label>
            <input
              type="password"
              name="password"
              id="password"
              value={formData.password}
              onChange={handeInputChange}
            />
          </div>

          {/* First Name Field */}
          <div>
            <label htmlFor="first_name">First Name</label>
            <input
              type="text"
              name="first_name"
              id="first_name"
              value={formData.first_name}
              onChange={handeInputChange}
            />
          </div>

          {/* Last Name Field */}
          <div>
            <label htmlFor="last_name">Last Name</label>
            <input
              type="text"
              name="last_name"
              id="last_name"
              value={formData.last_name}
              onChange={handeInputChange}
            />
          </div>

          {/* Profile Field */}
          <div>
            <label htmlFor="profile">Avatar</label>
            <input
              type="file"
              accept="images/*"
              name="profile"
              id="profile"
              onChange={handleImage}
            />
            {formData.showProfile && (
              <img
                src={formData.showProfile}
                alt=""
                className="size-30 rounded-full"
              />
            )}
          </div>
        </section>

        {/* Action Control */}
        <div className="flex gap-5 justify-center">
          <button type="submit" className="bg-green-800 cursor-pointer">
            Submit
          </button>
          <button
            onClick={() => setVisible(false)}
            type="button"
            className="bg-red-800 cursor-pointer"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
