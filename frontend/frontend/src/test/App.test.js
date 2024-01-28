import React from "react";
import { configure, shallow } from "enzyme";
import { expect } from "chai";
import chaiEnzyme from "chai-enzyme";
import Adapter from "enzyme-adapter-react-16";
import App from "../App";

configure({
   adapter: new Adapter(),
});

describe("Testing <App/> Component", () => {
   it("App renders a message", async () => {
      const wrapper = shallow(<App />);
      const message = (
         <p>
            Edit <code>src/App.js</code> and save to reload.
         </p>
      );
      expect(wrapper).to.contain(message);
   });

   const chai = await import("chai");
   chai.use(chaiEnzyme());
});
