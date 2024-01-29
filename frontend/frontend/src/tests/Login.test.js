import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import axios from "axios";
import Cookies from "js-cookie";
import { BrowserRouter as Router } from "react-router-dom";
import Login from "../components/Login";
import { reloadPage } from "../utils";

jest.mock("axios");
jest.mock("../utils");

describe("Login Component", () => {
  test("renders login form when not authenticated", () => {
    render(
      <Router>
        <Login setCurrentUserID={() => {}} />
      </Router>
    );

    // Check if form elements are rendered
    expect(screen.getByLabelText(/Username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Password/i)).toBeInTheDocument();
    expect(screen.getByText(/Login/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Submit/i })).toBeInTheDocument();
  });

  test("submits login form and navigates on success", async () => {
    axios.post.mockResolvedValue({ data: { access_token: "testToken" } });

    const setCurrentUserID = jest.fn();

    render(
      <Router>
        <Login setCurrentUserID={setCurrentUserID} />
      </Router>
    );

    // Simulate user input
    fireEvent.change(screen.getByLabelText(/Username/i), {
      target: { value: "testUser" },
    });
    fireEvent.change(screen.getByLabelText(/Password/i), {
      target: { value: "testPassword" },
    });

    // Submit the form
    fireEvent.click(screen.getByRole("button", { name: /Submit/i }));

    // Wait for the navigation to occur
    await waitFor(() => {
      expect(setCurrentUserID).toHaveBeenCalledWith("testToken");
    });

    // Ensure that the navigation has occurred
    expect(window.location.pathname).toEqual("/");
    expect(localStorage.getItem("isAuth")).toEqual("false");
  });

  test("shows alert on login failure", async () => {
    axios.post.mockRejectedValue({
      response: { data: "Incorrect Username or password" },
    });

    render(
      <Router>
        <Login setCurrentUserID={() => {}} />
      </Router>
    );

    // Simulate user input
    fireEvent.change(screen.getByLabelText(/Username/i), {
      target: { value: "testUser" },
    });

    fireEvent.change(screen.getByLabelText(/Password/i), {
      target: { value: "testPassword" },
    });
    // Submit the form
    fireEvent.click(screen.getByRole("button", { name: /Submit/i }));

    // Wait for the alert to appear
    await waitFor(() => {
      expect(
        screen.getByText(/Incorrect Username or password/i)
      ).toBeInTheDocument();
    });
  });
});
