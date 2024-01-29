import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "../App";

test("renders Home, Register, and Login links when not authenticated", () => {
  render(<App />);

  const homeLink = screen.getByText(/Home/i, { selector: 'a[href="/"]' });
  const registerLink = screen.getByText(/Register/i);
  const loginLink = screen.getByText(/Login/i);

  expect(homeLink).toBeInTheDocument();
  expect(registerLink).toBeInTheDocument();
  expect(loginLink).toBeInTheDocument();

  // Check if "Goals" and "Profile" links are not present
  expect(screen.queryByText(/Goals/i)).toBeNull();
  expect(screen.queryByText(/Profile/i)).toBeNull();
});

test("renders Home, Goals, Profile, and Logout links when authenticated", () => {
  // Mock localStorage to simulate an authenticated state
  Object.defineProperty(window, "localStorage", {
    value: {
      getItem: jest.fn(() => "true"),
    },
    writable: true,
  });

  render(<App />);

  const homeLink = screen.getByText(/Home/i, { selector: 'a[href="/"]' });
  const goalsLink = screen.getByText(/Goals/i);
  const profileLink = screen.getByText(/Profile/i);

  expect(homeLink).toBeInTheDocument();
  expect(goalsLink).toBeInTheDocument();
  expect(profileLink).toBeInTheDocument();

  // Check if "Register" and "Login" links are not present
  expect(screen.queryByText(/Register/i)).toBeNull();
  expect(screen.queryByText(/Login/i)).toBeNull();

  // Switch to authenticated state
  userEvent.click(homeLink);

  // Check if "Home" is rendered in AllLinks after the click
  const homeLinkAllLinks = screen.queryByText(/Home/i, {
    selector: 'a[href="/"]',
  });
  expect(homeLinkAllLinks).toBeInTheDocument();
});
