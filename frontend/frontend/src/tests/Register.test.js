import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import axios from "axios";
import Register from "../components/Register";

jest.mock("axios"); // Mocking axios module

describe("Register Component", () => {
  test("renders register form when not authenticated", () => {
    render(<Register />);

    // Check if form elements are rendered
    expect(screen.getByLabelText(/Username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Password/i)).toBeInTheDocument();
    expect(screen.getByText(/Register Yourself/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Submit/i })).toBeInTheDocument();
  });

  test("submits registration form and shows success alert", async () => {
    axios.post.mockResolvedValue({ data: "Successfully Registered" });

    render(<Register />);

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
      expect(screen.getByText(/Successfully Registered/i)).toBeInTheDocument();
    });
  });

  test("submits registration form and shows error alert", async () => {
    axios.post.mockRejectedValue({ response: { data: "User Already Exists" } });

    render(<Register />);

    // Simulate user input
    fireEvent.change(screen.getByLabelText(/Username:/i), {
      target: { value: "existingUser" },
    });
    fireEvent.change(screen.getByLabelText(/Password:/i), {
      target: { value: "testPassword" },
    });

    // Submit the form
    fireEvent.click(screen.getByRole("button", { name: /Submit/i }));

    // Wait for the alert to appear
    await waitFor(() => {
      expect(screen.getByText(/User Already Exists/i)).toBeInTheDocument();
    });
  });
});
