import axios from "axios";

const BASE_URL = "http://localhost:8000/api/app/contact";

export const fetchTenantName = async (tenantId) => {
  try {
    const responseTenantName = await axios.get(`${BASE_URL}/tenantName`, {
      headers: {
        "Content-Type": "application/json",
        tenantId: tenantId,
      },
    });
    return responseTenantName.data;
  } catch (error) {
    console.error("Error fetching TenantName - API response", error);
    throw new Error("Error fetching TenantName - API response", error);
  }
};

export const fetchReasons = async (tenantId) => {
  try {
    const responseReasons = await axios.get(`${BASE_URL}/reasons`, {
      headers: {
        "Content-Type": "application/json",
        tenantId: tenantId,
      },
    });
    return responseReasons.data;
  } catch (error) {
    console.error("Error fetching Reasons - API response", error);
    throw new Error("Error fetching Reasons - API response", error);
  }
};

export const fetchRelated = async (tenantId) => {
  try {
    const responseRelated = await axios.get(`${BASE_URL}/related`, {
      headers: {
        "Content-Type": "application/json",
        tenantId: tenantId,
      },
    });
    return responseRelated.data;
  } catch (error) {
    console.error("Error fetching Related - API response", error);
    throw new Error("Error fetching Related - API response", error);
  }
};

export const submitForm = async (tenantId, formData) => {
  try {
    const responseSubmit = await axios.post(`${BASE_URL}`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        tenantId: tenantId,
      },
    });
    return responseSubmit.data;
  } catch (error) {
    console.error("Error to send Form - API", error);
    throw new Error("Error to send Form - API", error);
  }
};
