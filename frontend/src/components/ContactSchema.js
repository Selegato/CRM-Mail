import { object, string, number, bool } from "yup";

// Função para validar CPF
const isValidCPF = (cpf) => {
  cpf = cpf.replace(/[^\d]+/g, "");
  if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) return false;
  let sum = 0;
  let remainder;
  for (let i = 1; i <= 9; i++)
    sum += parseInt(cpf.substring(i - 1, i)) * (11 - i);
  remainder = (sum * 10) % 11;
  if (remainder === 10 || remainder === 11) remainder = 0;
  if (remainder !== parseInt(cpf.substring(9, 10))) return false;
  sum = 0;
  for (let i = 1; i <= 10; i++)
    sum += parseInt(cpf.substring(i - 1, i)) * (12 - i);
  remainder = (sum * 10) % 11;
  if (remainder === 10 || remainder === 11) remainder = 0;
  if (remainder !== parseInt(cpf.substring(10, 11))) return false;
  return true;
};

// Definição dos esquemas de validação para cada campo
const documentNumber = string()
  .required("* CPF is a required field")
  .test("is-valid-cpf", "* CPF not valid", (value) => isValidCPF(value));
const documentType = number().required();
const name = string()
  .required("* Name is a required field")
  .min(2, "* Name must have at least 2 characters")
  .matches(/^[a-zA-ZÀ-ÿ\s]+$/, "* Name must contain only Latin characters");
const lastName = string()
  .required("* Last name is a required field")
  .min(2, "* Last name must have at least 2 characters")
  .matches(
    /^[a-zA-ZÀ-ÿ\s]+$/,
    "* Last name must contain only Latin characters"
  );
const email = string()
  .email("* E-mail must be a valid e-mail address")
  .required("* E-mail is a required field");
const phone = string();
const celPhone = string().required("* Mobile is a required field");
const description = string()
  .min(50, "* Message must have at least 50 characters")
  .max(1000, "* Message must have at most 1000 characters")
  .required("* Message is a required field")
  .matches(
    /^[\u0000-\u007F\u00A0-\u00FF\p{P}\p{S}\s]+$/u,
    "* Message must contain only Latin characters"
  );

const contactReason = string().required(
  "* Reason for contact is a required field"
);
const contactRelatedTo = string().required(
  "* Related to is a required field"
);
const isPrime = bool().default(false).required();
const isMobile = bool().default(false).required();

export const ContactSchema = object({
  documentNumber,
  documentType,
  name,
  lastName,
  email,
  phone,
  celPhone,
  description,
  contactReason,
  contactRelatedTo,
  isPrime,
  isMobile,
});
